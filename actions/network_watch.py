"""Bounded Windows connectivity watcher."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def network_watch(parameters=None,**kwargs):
 p=parameters or {}; host=str(p.get("host","1.1.1.1")).strip()
 if len(host)>255 or not host:return "Valid host required."
 r=subprocess.run(["ping.exe","-n","2","-w","1500",host],capture_output=True,text=True,timeout=6,creationflags=subprocess.CREATE_NO_WINDOW)
 ok=r.returncode==0
 return f"Connectivity to {host}: {'ONLINE' if ok else 'OFFLINE'}\n"+(r.stdout or r.stderr)[-3000:]
TOOL={"name":"network_watch","description":"Windows-only connectivity check using bounded ping; useful for deciding whether a network problem is local or upstream. It does not modify network settings.","parameters":{"type":"OBJECT","properties":{"host":{"type":"STRING"}},"required":[]},"handler":network_watch}
