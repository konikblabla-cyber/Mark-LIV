"""Wait for a Windows process to become responsive."""
import platform,time,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_wait_ready(parameters=None,**kwargs):
 p=parameters or {}; name=str(p.get("process") or "").strip().lower(); timeout=max(1,min(int(p.get("timeout",30)),120))
 if not name:return "Missing process name."
 end=time.time()+timeout
 while time.time()<end:
  for x in psutil.process_iter(["name","pid","status"]):
   try:
    if (x.info["name"] or "").lower()==name and x.info["status"] not in (psutil.STATUS_ZOMBIE,):
     return f"Process responsive enough for automation: {x.info['name']} (PID {x.info['pid']}, status={x.info['status']})."
   except (psutil.NoSuchProcess,psutil.AccessDenied): pass
  time.sleep(.5)
 return f"Process not ready after {timeout}s: {name}"
TOOL={"name":"windows_process_wait_ready","description":"Wait for a Windows process to appear in a usable non-zombie state before continuing automation.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["process"]},"handler":windows_process_wait_ready}
