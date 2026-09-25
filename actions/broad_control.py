import os
import platform
import subprocess
import shlex
from core import confirm

# Optional: without core/permissions.py, actions still work normally.
try:
    from core.permissions import needs_confirmation
except (ImportError, ModuleNotFoundError):
    def needs_confirmation(action: str, *, admin: bool = False) -> bool:
        return False

_OS = platform.system()

def _execute(op, value=""):
    if _OS != "Windows":
        return "Windows control is currently supported only on Windows."
    if op == "launch":
        subprocess.Popen(shlex.split(value, posix=False), shell=False)
        return f"Launched: {value}"
    if op == "open_file":
        os.startfile(value)
        return f"Opened: {value}"
    if op == "open_folder":
        os.startfile(value)
        return f"Opened folder: {value}"
    if op == "close_active":
        subprocess.run(["powershell", "-NoProfile", "-Command",
                        "(New-Object -ComObject WScript.Shell).SendKeys('%{F4}')"],
                       capture_output=True)
        return "Requested close of the active window."
    if op == "lock":
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], capture_output=True)
        return "PC locked."
    if op == "sleep":
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], capture_output=True)
        return "PC sleep requested."
    return f"Unknown operation: {op}"

def broad_control(parameters=None, response=None, player=None, session_memory=None):
    p = parameters or {}
    op = str(p.get("operation", "")).strip().lower()
    value = str(p.get("value", "")).strip()
    allowed = {"launch", "open_file", "open_folder", "close_active", "lock", "sleep"}
    if op not in allowed:
        return "Choose a supported operation: launch, open_file, open_folder, close_active, lock, sleep."
    if op in {"launch", "open_file", "open_folder"} and not value:
        return "A target is required."

    if needs_confirmation(op):
        if confirm.pending_title():
            return "There is already a confirmation waiting on screen."
        return confirm.request(
            key=f"broad_control:{op}",
            title="Allow JARVIS to perform this computer action?",
            detail=f"Operation: {op}\nTarget: {value or '(current computer)'}",
            run=lambda: _execute(op, value),
        )
    return _execute(op, value)

TOOL = {
    "name": "broad_control",
    "description": "Windows computer control. Normal actions execute directly; operations listed in the optional central permissions policy require human confirmation.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {"type": "STRING", "description": "One of: launch, open_file, open_folder, close_active, lock, sleep."},
            "value": {"type": "STRING", "description": "Program, file, folder, or other target."}
        },
        "required": ["operation"]
    },
    "handler": broad_control,
}
