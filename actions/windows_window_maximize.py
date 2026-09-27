"""Maximize the foreground Windows window."""
import ctypes,platform
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_maximize(parameters=None,**kwargs):
 if not kwargs.get("_permission_token"):
  p=dict(parameters or {});d,r=permission_decision("windows_window_maximize",p)
  if d=="deny":return f"Permission denied: {r}"
  if d=="confirm":return confirm.request(key="windows_window_maximize",title="Allow JARVIS: windows_window_maximize?",detail=f"{r}. Waiting for your confirmation.",run=lambda:windows_window_maximize(p,_permission_token=True))
 u=ctypes.windll.user32;h=u.GetForegroundWindow()
 if not h:return "No foreground window."
 u.ShowWindow(h,3);return "Foreground window maximized."
TOOL={"name":"windows_window_maximize","description":"Maximize the current foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_window_maximize}
