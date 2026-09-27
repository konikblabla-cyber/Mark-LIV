"""Switch Windows virtual desktops using normal keyboard shortcuts."""
import platform,pyautogui
from core.permissions import permission_decision
from core import confirm
def windows_desktop_switch(parameters=None,_permission_token=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 if _permission_token is None:
  decision,reason=permission_decision("windows_desktop_switch",parameters or {})
  if decision=="deny":return f"Permission denied: {reason}"
  if decision=="confirm":return confirm.request(key="windows_desktop_switch",title="Allow JARVIS: windows_desktop_switch?",detail=f"{reason}. Waiting for your confirmation.",run=lambda:windows_desktop_switch(parameters or {},_permission_token=True))
 p=parameters or {}; direction=str(p.get("direction","right")).lower()
 if direction not in ("left","right"): return "Direction must be left or right."
 pyautogui.hotkey("win","ctrl","right" if direction=="right" else "left")
 return f"Switched virtual desktop {direction}."
TOOL={"name":"windows_desktop_switch","description":"Switch Windows virtual desktops left or right using Win+Ctrl+Arrow.","parameters":{"type":"OBJECT","properties":{"direction":{"type":"STRING"}}},"handler":windows_desktop_switch}
