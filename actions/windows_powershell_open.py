"""Open a normal Windows PowerShell session."""
import platform,subprocess
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_powershell_open(parameters=None,**kwargs):

             if not kwargs.get("_permission_token"):
                 p = dict(parameters or {})
                 decision, reason = permission_decision("windows_powershell_open", p)
                 if decision == "deny":
                     return f"Permission denied: {reason}"
                 if decision == "confirm":
                     return confirm.request(key="windows_powershell_open", title="Allow JARVIS: windows_powershell_open?", detail=f"{reason}. Waiting for your confirmation.", run=lambda: windows_powershell_open(p, _permission_token=True))
    p=parameters or {}; command=str(p.get("command") or "").strip()
    args=["powershell.exe","-NoLogo"]
    if command: args += ["-NoExit","-Command",command]
    subprocess.Popen(args,shell=False)
    return "Opened Windows PowerShell normally."
TOOL={"name":"windows_powershell_open","description":"Open a normal Windows PowerShell session, optionally with an initial command; uses normal Windows permissions.","parameters":{"type":"OBJECT","properties":{"command":{"type":"STRING"}}},"handler":windows_powershell_open}
