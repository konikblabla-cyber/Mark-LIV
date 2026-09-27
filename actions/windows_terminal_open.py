"""Open a Windows terminal in a directory."""
import platform,subprocess
from core.permissions import permission_decision
from core import confirm
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_terminal_open(parameters=None,**kwargs):

    if not kwargs.get("_permission_token"):
        p = dict(parameters or {})
        decision, reason = permission_decision("windows_terminal_open", p)
        if decision == "deny":
            return f"Permission denied: {reason}"
        if decision == "confirm":
            return confirm.request(key="windows_terminal_open", title="Allow JARVIS: windows_terminal_open?", detail=f"{reason}. Waiting for your confirmation.", run=lambda: windows_terminal_open(p, _permission_token=True))
    p=parameters or {}; directory=Path(str(p.get("directory") or Path.home())).expanduser()
    if not directory.is_dir():return f"Directory not found: {directory}"
    subprocess.Popen(["wt.exe","-d",str(directory)],shell=False)
    return f"Opened Windows Terminal in {directory}."
TOOL={"name":"windows_terminal_open","description":"Open Windows Terminal in an existing directory.","parameters":{"type":"OBJECT","properties":{"directory":{"type":"STRING"}}},"handler":windows_terminal_open}
