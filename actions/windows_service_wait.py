"""Wait for a Windows service to reach a requested state."""
import platform,time,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_service_wait(parameters=None,**kwargs):
 p=parameters or {}; name=str(p.get("service") or "").strip(); wanted=str(p.get("state","running")).lower(); timeout=max(1,min(int(p.get("timeout",30)),120))
 if not name:return "Missing service name."
 if wanted not in ("running","stopped"):return "State must be running or stopped."
 end=time.time()+timeout
 while time.time()<end:
  r=subprocess.run(["sc","query",name],capture_output=True,text=True,encoding="utf-8",errors="replace")
  out=r.stdout.upper()
  if ("RUNNING" in out if wanted=="running" else "STOPPED" in out):return f"Service {name} is {wanted}."
  time.sleep(.5)
 return f"Service {name} did not reach {wanted} within {timeout}s."
TOOL={"name":"windows_service_wait","description":"Wait for a Windows service to become running or stopped.","parameters":{"type":"OBJECT","properties":{"service":{"type":"STRING"},"state":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["service"]},"handler":windows_service_wait}
