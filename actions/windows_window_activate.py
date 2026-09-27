"""Activate a uniquely matched visible Windows window."""
import ctypes,platform
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_activate(parameters=None,**kwargs):
 if not kwargs.get("_permission_token"):
  p=dict(parameters or {});d,r=permission_decision("windows_window_activate",p)
  if d=="deny":return f"Permission denied: {r}"
  if d=="confirm":return confirm.request(key="windows_window_activate",title="Allow JARVIS: windows_window_activate?",detail=f"{r}. Waiting for your confirmation.",run=lambda:windows_window_activate(p,_permission_token=True))
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower()
 if not needle:return "Missing window title text."
 u=ctypes.windll.user32; matches=[]
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long)
 def cb(h,l):
  if u.IsWindowVisible(h):
   n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
   if needle in b.value.lower():matches.append((h,b.value))
  return True
 u.EnumWindows(W(cb),0)
 if len(matches)!=1:return f"Expected one matching window, found {len(matches)}."
 h,title=matches[0];u.ShowWindow(h,5);u.SetForegroundWindow(h)
 return f"Activated: '{title}'."
TOOL={"name":"windows_window_activate","description":"Activate one uniquely matched visible Windows window by title text.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"}},"required":["contains"]},"handler":windows_window_activate}
