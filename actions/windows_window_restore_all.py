"""Restore all minimized visible top-level Windows windows."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
SW_RESTORE=9
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_restore_all(parameters=None,**kwargs):
 u=ctypes.windll.user32;count=0
 def cb(hwnd,lparam):
  nonlocal count
  if u.IsWindowVisible(hwnd) and u.IsIconic(hwnd):u.ShowWindow(hwnd,SW_RESTORE);count+=1
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 return f"Restored {count} minimized window(s)."
TOOL={"name":"windows_window_restore_all","description":"Restore all currently minimized visible top-level Windows windows.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_window_restore_all}
