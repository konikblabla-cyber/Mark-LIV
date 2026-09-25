"""Wait for a Windows application process to exit."""
import platform,time,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_app_exit_wait(parameters=None,**kwargs):
 p=parameters or {}; name=str(p.get("process") or "").strip().lower(); timeout=max(1,min(int(p.get("timeout",30)),120))
 if not name:return "Missing process name."
 end=time.time()+timeout
 while time.time()<end:
  alive=False
  for x in psutil.process_iter(["name"]):
   try:
    if (x.info["name"] or "").lower()==name: alive=True; break
   except (psutil.NoSuchProcess,psutil.AccessDenied): pass
  if not alive:return f"Application exited: {name}."
  time.sleep(.5)
 return f"Application still running after {timeout}s: {name}"
TOOL={"name":"windows_app_exit_wait","description":"Wait for a named Windows process to exit, bounded to 120 seconds.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["process"]},"handler":windows_app_exit_wait}
