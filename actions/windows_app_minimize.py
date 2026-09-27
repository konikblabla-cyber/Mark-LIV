"""Minimize a uniquely matched Windows window."""
import ctypes,platform
from core.permissions import permission_decision
from core import confirm
def windows_app_minimize(parameters=None,**kwargs):
 if not kwargs.get("_permission_token"):
  p=dict(parameters or {});d,r=permission_decision("windows_app_minimize",p)
  if d=="deny":return f"Permission denied: {r}"
  if d=="confirm":return confirm.request(key="windows_app_minimize",title="Allow JARVIS: windows_app_minimize?",detail=f"{r}. Waiting for your confirmation.",run=lambda:windows_app_minimize(p,_permission_token=True))
 if platform.system()!="Windows": return "Windows-only action."
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
 h,title=matches[0];u.ShowWindow(h,6);return f"Minimized: '{title}'."
TOOL={"name":"windows_app_minimize","description":"Minimize one uniquely matched visible Windows window.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"}},"required":["contains"]},"handler":windows_app_minimize}