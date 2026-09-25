"""Bounded Windows connectivity watcher."""
import platform,subprocess
def network_watch(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; host=str(p.get("host","1.1.1.1")).strip()
 if len(host)>255 or not host:return "Valid host required."
 try:
  r=subprocess.run(["ping.exe","-n","2","-w","1500",host],capture_output=True,text=True,timeout=6,creationflags=subprocess.CREATE_NO_WINDOW)
 except (subprocess.TimeoutExpired,OSError) as e:
  return f"Connectivity check failed: {e}"
 ok=r.returncode==0
 return f"Connectivity to {host}: {'ONLINE' if ok else 'OFFLINE'}\n"+(r.stdout or r.stderr)[-3000:]
TOOL={"name":"network_watch","description":"Windows-only connectivity check using bounded ping; useful for deciding whether a network problem is local or upstream. It does not modify network settings.","parameters":{"type":"OBJECT","properties":{"host":{"type":"STRING"}},"required":[]},"handler":network_watch}
