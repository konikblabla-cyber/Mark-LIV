"""Read-only mapping between Windows windows and their processes."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_process(parameters=None,**kwargs):
 p=parameters or {}; title=str(p.get("title","")).strip().lower()
 if not title:return "Window title is required."
 u=ctypes.windll.user32; rows=[]
 def cb(hwnd,lparam):
  if u.IsWindowVisible(hwnd):
   n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
   if title in b.value.lower():
    pid=ctypes.c_ulong();u.GetWindowThreadProcessId(hwnd,ctypes.byref(pid));rows.append((b.value,pid.value))
  return True
 u.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_void_p)(cb),0)
 return "\n".join(f"Title={t} PID={pid}" for t,pid in rows[:20]) or "Window not found."
TOOL={"name":"windows_window_process","description":"Read-only mapping of a visible Windows window title to its owning process ID.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}},"required":["title"]},"handler":windows_window_process}
