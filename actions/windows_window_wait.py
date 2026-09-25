"""Bounded wait for a Windows window title or process to appear."""
import platform,ctypes,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_wait(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("title","")).strip().lower(); seconds=max(1,min(int(p.get("seconds",20)),120))
 if not needle:return "Window title is required."
 u=ctypes.windll.user32; found=None; end=time.time()+seconds
 while time.time()<end:
  rows=[]
  def cb(hwnd,lparam):
   if u.IsWindowVisible(hwnd):
    n=u.GetWindowTextLengthW(hwnd)
    if n:
     b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
     if needle in b.value.lower():rows.append((hwnd,b.value))
   return True
  u.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_void_p)(cb),0)
  if rows:return "\n".join(f"HWND={h} Title={t}" for h,t in rows[:10])
  time.sleep(.5)
 return "Window not found before timeout."
TOOL={"name":"windows_window_wait","description":"Bounded wait for a visible Windows window whose title contains the requested text.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"},"seconds":{"type":"INTEGER"}},"required":["title"]},"handler":windows_window_wait}
