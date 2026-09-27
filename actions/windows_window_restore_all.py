"""Restore all minimized visible top-level Windows windows."""
import ctypes,platform
from core.permissions import permission_decision
from core import confirm
_TOKEN = object()
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
SW_RESTORE=9
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_restore_all(parameters=None,**kwargs):
 if kwargs.get("_permission_token") is not _TOKEN:
  p=dict(parameters or {})
  decision,reason=permission_decision("windows_window_restore_all",p)
  if decision=="deny": return f"Permission denied: {reason}"
  if decision=="confirm":
   if confirm.pending_title(): return "There is already a confirmation waiting. Ask the user to answer it first."
   return confirm.request(key="windows_window_restore_all",title="Allow JARVIS: windows_window_restore_all?",detail=f"{reason}. JARVIS will wait for your confirmation before executing it.",run=lambda: windows_window_restore_all(p,_permission_token=_TOKEN))
 u=ctypes.windll.user32;count=0
 def cb(hwnd,lparam):
  nonlocal count
  if u.IsWindowVisible(hwnd) and u.IsIconic(hwnd):u.ShowWindow(hwnd,SW_RESTORE);count+=1
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 return f"Restored {count} minimized window(s)."
TOOL={"name":"windows_window_restore_all","description":"Restore all currently minimized visible top-level Windows windows.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_window_restore_all}
