"""Open a normal Windows PowerShell session."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_powershell_open(parameters=None,**kwargs):
 p=parameters or {}; command=str(p.get("command") or "").strip()
 args=["powershell.exe","-NoLogo"]
 if command: args += ["-NoExit","-Command",command]
 subprocess.Popen(args,shell=False)
 return "Opened Windows PowerShell normally."
TOOL={"name":"windows_powershell_open","description":"Open a normal Windows PowerShell session, optionally with an initial command; uses normal Windows permissions.","parameters":{"type":"OBJECT","properties":{"command":{"type":"STRING"}}},"handler":windows_powershell_open}
