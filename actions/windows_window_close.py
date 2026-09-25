"""Targeted Windows window close action."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_close(parameters=None,**kwargs):
 p=parameters or {}; title=str(p.get("title","")).strip().lower()
 if not title:return "Window title is required."
 u=ctypes.windll.user32; found=[]
 def cb(hwnd,lparam):
  if u.IsWindowVisible(hwnd):
   n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
   if title in b.value.lower():found.append((hwnd,b.value))
  return True
 u.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_void_p)(cb),0)
 if not found:return "Window not found."
 if len(found)>1:return "Multiple matching windows: "+" | ".join(t for _,t in found[:10])
 u.PostMessageW(found[0][0],0x0010,0,0);return f"Close requested: {found[0][1]}"
TOOL={"name":"windows_window_close","description":"Request close of one uniquely matched visible Windows window by title; never force-kills the process.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}},"required":["title"]},"handler":windows_window_close}
