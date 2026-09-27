"""Restore a uniquely matched Windows window."""
import ctypes,platform
from core.permissions import permission_decision
from core import confirm
_TOKEN = object()
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_restore(parameters=None,**kwargs):
 if kwargs.get("_permission_token") is not _TOKEN:
  p=dict(parameters or {})
  decision,reason=permission_decision("windows_window_restore",p)
  if decision=="deny": return f"Permission denied: {reason}"
  if decision=="confirm":
   if confirm.pending_title(): return "There is already a confirmation waiting. Ask the user to answer it first."
   return confirm.request(key="windows_window_restore",title="Allow JARVIS: windows_window_restore?",detail=f"{reason}. JARVIS will wait for your confirmation before executing it.",run=lambda: windows_window_restore(p,_permission_token=_TOKEN))
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower()
 if not needle:return "Missing window title text."
 u=ctypes.windll.user32;matches=[];W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long)
 def cb(h,l):
  if u.IsWindowVisible(h):
   n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
   if needle in b.value.lower():matches.append((h,b.value))
  return True
 u.EnumWindows(W(cb),0)
 if len(matches)!=1:return f"Expected one matching window, found {len(matches)}."
 h,title=matches[0];u.ShowWindow(h,9);return f"Restored: '{title}'."
TOOL={"name":"windows_window_restore","description":"Restore one uniquely matched minimized Windows window.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"}},"required":["contains"]},"handler":windows_window_restore}
