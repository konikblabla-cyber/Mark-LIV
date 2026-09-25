"""Windows identity and session information for Mark-LIV."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_identity(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","user")).lower().strip()
 cmds={"user":"whoami","computer":"$env:COMPUTERNAME","session":"quser"}
 if a not in cmds:return "Use user, computer or session."
 exe=["powershell.exe","-NoProfile","-NonInteractive","-Command",cmds[a]] if a!="user" and a!="session" else ([ "whoami.exe"] if a=="user" else ["quser.exe"])
 r=subprocess.run(exe,capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No identity data.")[:5000]
TOOL={"name":"windows_identity","description":"Windows-only identity/session diagnostics: current Windows user, computer name, or logged-on session information.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_identity}
