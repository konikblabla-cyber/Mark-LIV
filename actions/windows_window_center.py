"""Center a Windows window on the primary display."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_center(parameters=None,**kwargs):
 p=parameters or {};title=str(p.get("title","")).strip()
 if not title:return "Window title is required."
 u=ctypes.windll.user32;found=[]
 def cb(x,_):
  if u.IsWindowVisible(x):
   n=u.GetWindowTextLengthW(x);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(x,b,n+1)
   if title.casefold() in b.value.casefold():found.append(x)
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 if not found:return f"No visible window matching '{title}'."
 r=ctypes.wintypes.RECT();u.GetWindowRect(found[0],ctypes.byref(r));w=r.right-r.left;h=r.bottom-r.top
 x=max(0,(u.GetSystemMetrics(0)-w)//2);y=max(0,(u.GetSystemMetrics(1)-h)//2)
 u.SetWindowPos(found[0],0,x,y,0,0,0x0001|0x0004);return f"Centered window at ({x},{y})."
TOOL={"name":"windows_window_center","description":"Center a uniquely matched visible Windows window on the primary display.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}},"required":["title"]},"handler":windows_window_center}
