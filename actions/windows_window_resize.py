"""Resize a Windows window."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_resize(parameters=None,**kwargs):
 p=parameters or {};title=str(p.get("title","")).strip();w=max(100,min(int(p.get("width",800)),7680));h=max(100,min(int(p.get("height",600)),4320))
 if not title:return "Window title is required."
 u=ctypes.windll.user32;found=[]
 def cb(x,_):
  if u.IsWindowVisible(x):
   n=u.GetWindowTextLengthW(x);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(x,b,n+1)
   if title.casefold() in b.value.casefold():found.append(x)
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 if not found:return f"No visible window matching '{title}'."
 u.SetWindowPos(found[0],0,0,0,w,h,0x0002|0x0001);return f"Resized window to {w}x{h}."
TOOL={"name":"windows_window_resize","description":"Resize a uniquely matched visible Windows window with bounded dimensions.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"},"width":{"type":"INTEGER"},"height":{"type":"INTEGER"}},"required":["title","width","height"]},"handler":windows_window_resize}
