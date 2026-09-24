import os
import platform
import subprocess
from pathlib import Path
from core import confirm

_OS = platform.system()

def _execute(op, value=""):
    if _OS != "Windows":
        return "Windows control is currently supported only on Windows."

    if op == "launch":
        subprocess.Popen(value, shell=True)
        return f"Launched: {value}"
    if op == "open_file":
        os.startfile(value)
        return f"Opened: {value}"
    if op == "open_folder":
        os.startfile(value)
        return f"Opened folder: {value}"
    if op == "close_active":
        subprocess.run(["taskkill", "/PID", str(os.getpid()), "/T"], capture_output=True)
        return "Requested application close."
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

    if confirm.pending_title():
        return "There is already a confirmation waiting on screen."

    return confirm.request(
        key="broad_control",
        title="Allow JARVIS to perform this computer action?",
        detail=f"Operation: {op}\nTarget: {value or '(current computer)'}",
        run=lambda: _execute(op, value),
    )

TOOL = {
    "name": "broad_control",
    "description": "Confirmed Windows computer control for launching programs, opening files/folders, locking and sleeping the PC. Every operation requires an explicit human confirmation.",
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
