"""Windows application inventory based on visible windows."""
import platform,ctypes
from ctypes import wintypes
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_apps_running(parameters=None,**kwargs):
 out=[]; cbtype=ctypes.WINFUNCTYPE(ctypes.c_bool,wintypes.HWND,wintypes.LPARAM); u=ctypes.windll.user32
 def cb(hwnd,_):
  if u.IsWindowVisible(hwnd):
   n=u.GetWindowTextLengthW(hwnd)
   if n:
    b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1);out.append(b.value)
  return True
 u.EnumWindows(cbtype(cb),0)
 return "\n".join(dict.fromkeys(out))[:12000] or "No visible applications."
TOOL={"name":"windows_apps_running","description":"Read-only list of currently visible Windows application windows.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_apps_running}
