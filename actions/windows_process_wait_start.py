"""Wait for a Windows process to appear, then return its PID."""
import platform,time,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_wait_start(parameters=None,**kwargs):
 p=parameters or {};name=str(p.get("process") or "").strip().lower()
 timeout=max(1,min(int(p.get("timeout",30)),120))
 if not name:return "Missing process name."
 end=time.time()+timeout
 while time.time()<end:
  for x in psutil.process_iter(["name","pid"]):
   try:
    if (x.info["name"] or "").lower()==name:return f"Started: {x.info['name']} (PID {x.info['pid']})."
   except (psutil.NoSuchProcess,psutil.AccessDenied):pass
  time.sleep(.25)
 return f"Process did not start within {timeout}s: {name}"
TOOL={"name":"windows_process_wait_start","description":"Wait for a named Windows process to start and return its PID.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["process"]},"handler":windows_process_wait_start}
