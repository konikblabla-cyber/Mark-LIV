"""Find visible Windows windows belonging to a process."""
import ctypes,platform,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_window_title(parameters=None,**kwargs):
 p=parameters or {}; target=str(p.get("process") or "").strip().lower()
 if not target:return "Missing process name."
 found=[]
 u=ctypes.windll.user32
 def cb(hwnd,lparam):
  if not u.IsWindowVisible(hwnd): return True
  pid=ctypes.c_ulong();u.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
  try:
   if (psutil.Process(pid.value).name() or "").lower()==target:
    n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
    if b.value: found.append(f"{pid.value}: {b.value}")
  except (psutil.NoSuchProcess,psutil.AccessDenied): pass
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 return "\n".join(found) if found else f"No titled visible window for {target}."
TOOL={"name":"windows_process_window_title","description":"List visible titled Windows owned by a named process.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"}},"required":["process"]},"handler":windows_process_window_title}
