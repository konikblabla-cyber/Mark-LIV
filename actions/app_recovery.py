"""Windows app health and controlled restart helper."""
import platform,subprocess,psutil,os
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def app_recovery(parameters=None,**kwargs):
 p=parameters or {}; exe=os.path.basename(str(p.get("exe","")).strip())
 if not exe:return "Executable name required."
 matches=[x for x in psutil.process_iter(["pid","name","status"]) if (x.info.get("name") or "").casefold()==exe.casefold()]
 if not matches:return f"{exe} is not running."
 bad=[]
 for x in matches:
  try:
   if x.status() in (psutil.STATUS_ZOMBIE,psutil.STATUS_DEAD):bad.append(x.pid)
  except (psutil.NoSuchProcess,psutil.AccessDenied):pass
 if not bad:return f"{exe} is running normally (PIDs: {', '.join(str(x.pid) for x in matches)})."
 return f"{exe} has unhealthy process state(s): {', '.join(map(str,bad))}. Restart manually if needed."
TOOL={"name":"app_recovery","description":"Read-only Windows app recovery check using process state; identifies unhealthy process states without killing or restarting anything automatically.","parameters":{"type":"OBJECT","properties":{"exe":{"type":"STRING"}},"required":["exe"]},"handler=app_recovery}
