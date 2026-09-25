"""Count visible Windows windows owned by a process."""
import ctypes,platform,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_window_count(parameters=None,**kwargs):
 p=parameters or {}; target=str(p.get("process") or "").strip().lower()
 if not target:return "Missing process name."
 u=ctypes.windll.user32; pids={x.pid for x in psutil.process_iter() if (x.info.get("name") or "").lower()==target} if False else set()
 for x in psutil.process_iter(["name"]):
  try:
   if (x.info["name"] or "").lower()==target:pids.add(x.pid)
  except (psutil.NoSuchProcess,psutil.AccessDenied):pass
 count=0
 def cb(h,l):
  nonlocal count
  if u.IsWindowVisible(h):
   pid=ctypes.c_ulong();u.GetWindowThreadProcessId(h,ctypes.byref(pid))
   if pid.value in pids:count+=1
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 return f"{target}: {count} visible window(s)."
TOOL={"name":"windows_process_window_count","description":"Count visible top-level Windows windows owned by a named process.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"}},"required":["process"]},"handler":windows_process_window_count}
