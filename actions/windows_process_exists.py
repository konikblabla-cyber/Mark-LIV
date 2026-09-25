"""Read-only Windows process existence check."""
import platform,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_exists(parameters=None,**kwargs):
 p=parameters or {}; name=str(p.get("process") or "").strip().lower()
 if not name:return "Missing process name."
 found=[]
 for x in psutil.process_iter(["pid","name"]):
  try:
   if (x.info["name"] or "").lower()==name:found.append(x.info["pid"])
  except (psutil.NoSuchProcess,psutil.AccessDenied):pass
 return f"{name}: running, PIDs={found}" if found else f"{name}: not running."
TOOL={"name":"windows_process_exists","description":"Check whether a named Windows process is currently running.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"}},"required":["process"]},"handler":windows_process_exists}
