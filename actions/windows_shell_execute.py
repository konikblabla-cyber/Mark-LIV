"""Controlled Windows shell utility for harmless command-line queries."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
ALLOWED={"whoami":["whoami.exe"],"hostname":["hostname.exe"],"ver":["cmd.exe","/c","ver"],"date":["cmd.exe","/c","date","/t"],"time":["cmd.exe","/c","time","/t"]}
def windows_shell_execute(parameters=None,**kwargs):
 a=str((parameters or {}).get("action","")).lower().strip()
 if a not in ALLOWED:return "Allowed actions: whoami, hostname, ver, date, time."
 r=subprocess.run(ALLOWED[a],capture_output=True,text=True,timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No output.")[:3000]
TOOL={"name":"windows_shell_execute","description":"Read-only Windows shell queries limited to identity, hostname, OS version, date and time.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_shell_execute}
