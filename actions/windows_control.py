"""Broad Windows control surface for JARVIS.

The optional core.permissions module decides which operations need a human
confirmation. If it is absent, this action still works normally.
Windows UAC remains the OS-level boundary for administrator operations.
"""

import os
import platform
import subprocess
from pathlib import Path

from core import confirm

try:
    from core.permissions import needs_confirmation
except (ImportError, ModuleNotFoundError):
    def needs_confirmation(action: str, *, admin: bool = False) -> bool:
        return False

_OS = platform.system()


def _ps(command: str) -> str:
    r = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
        capture_output=True, text=True, timeout=30,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    return (r.stdout or r.stderr or "").strip()


def _execute(op: str, value: str) -> str:
    if _OS != "Windows":
        return "This control surface currently supports Windows only."

    if op == "run":
        r = subprocess.run(value, shell=True, capture_output=True, text=True, timeout=60)
        return (r.stdout or r.stderr or f"Command finished with code {r.returncode}").strip()

    if op == "run_admin":
        subprocess.Popen(["powershell", "-NoProfile", "-Command",
                          "Start-Process", "powershell", "-Verb", "RunAs",
                          "-ArgumentList", value])
        return "Administrator command started; Windows may show a UAC prompt."

    if op == "launch":
        subprocess.Popen(value, shell=True)
        return f"Launched: {value}"

    if op in {"open", "open_file", "open_folder"}:
        os.startfile(value)
        return f"Opened: {value}"

    if op == "list_processes":
        return _ps("Get-Process | Sort-Object ProcessName | Select-Object Id,ProcessName,MainWindowTitle | Format-Table -AutoSize | Out-String")

    if op == "list_windows":
        return _ps("Get-Process | Where-Object {$_.MainWindowHandle -ne 0} | Select-Object Id,ProcessName,MainWindowTitle | Format-Table -AutoSize | Out-String")

    if op == "kill_process":
        _ps(f"Stop-Process -Id {int(value)} -Force")
        return f"Process {value} terminated."

    if op == "close_process":
        _ps(f"Stop-Process -Id {int(value)}")
        return f"Close requested for process {value}."

    if op == "delete":
        p = Path(value).expanduser()
        if p.is_dir():
            import shutil
            shutil.rmtree(p)
        else:
            p.unlink()
        return f"Deleted: {p}"

    if op == "copy":
        import shutil
        shutil.copy2(Path(value.split("|", 1)[0]).expanduser(), Path(value.split("|", 1)[1]).expanduser())
        return "File copied."

    if op == "move":
        import shutil
        shutil.move(Path(value.split("|", 1)[0]).expanduser(), Path(value.split("|", 1)[1]).expanduser())
        return "Moved."

    if op == "mkdir":
        Path(value).expanduser().mkdir(parents=True, exist_ok=True)
        return f"Folder created: {value}"

    if op == "power":
        actions = {
            "lock": ["rundll32.exe", "user32.dll,LockWorkStation"],
            "sleep": ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
            "restart": ["shutdown", "/r", "/t", "0"],
            "shutdown": ["shutdown", "/s", "/t", "0"],
        }
        if value not in actions:
            return "power value must be lock, sleep, restart, or shutdown."
        subprocess.run(actions[value], capture_output=True)
        return f"Power action executed: {value}"

    if op == "open_settings":
        os.startfile("ms-settings:")
        return "Windows Settings opened."

    if op == "task_manager":
        subprocess.Popen(["taskmgr.exe"])
        return "Task Manager opened."

    return f"Unknown operation: {op}"


_CONFIRM_MAP = {
    "run": "execute_admin_command",
    "run_admin": "run_as_admin",
    "kill_process": "kill_process",
    "delete": "delete_file",
    "power": "restart",
}


def windows_control(parameters=None, response=None, player=None, session_memory=None):
    p = parameters or {}
    op = str(p.get("operation", "")).strip().lower()
    value = str(p.get("value", "")).strip()

    allowed = {
        "run", "run_admin", "launch", "open", "open_file", "open_folder",
        "list_processes", "list_windows", "kill_process", "close_process",
        "delete", "copy", "move", "mkdir", "power", "open_settings",
        "task_manager",
    }
    if op not in allowed:
        return "Unsupported operation."
    if op not in {"list_processes", "list_windows", "task_manager", "open_settings"} and not value:
        return "A value/target is required."

    policy_action = _CONFIRM_MAP.get(op)
    if op == "power" and value in {"restart", "shutdown"}:
        policy_action = value

    if policy_action and needs_confirmation(policy_action):
        if confirm.pending_title():
            return "There is already a confirmation waiting on screen."
        return confirm.request(
            key=f"windows_control:{op}",
            title=f"Allow JARVIS to perform: {op}?",
            detail=f"Target/value: {value or '(none)'}",
            run=lambda: _execute(op, value),
        )

    return _execute(op, value)


TOOL = {
    "name": "windows_control",
    "description": "Broad Windows control: launch/open apps and files, inspect processes/windows, close or terminate processes, create/copy/move/delete files, run commands, request admin commands through Windows UAC, power controls, and open Windows utilities. Risky operations use the optional central permission policy.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {"type": "STRING", "description": "run, run_admin, launch, open, open_file, open_folder, list_processes, list_windows, kill_process, close_process, delete, copy, move, mkdir, power, open_settings, task_manager"},
            "value": {"type": "STRING", "description": "Target, command, PID, path, or source|destination for copy/move."}
        },
        "required": ["operation"]
    },
    "handler": windows_control,
}
