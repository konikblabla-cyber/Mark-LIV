"""Open the standard Windows system menu for the foreground window."""
import platform,pyautogui
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_system_menu(parameters=None,**kwargs):
 if not kwargs.get("_permission_token"):
  p=dict(parameters or {});d,r=permission_decision("windows_system_menu",p)
  if d=="deny":return f"Permission denied: {r}"
  if d=="confirm":return confirm.request(key="windows_system_menu",title="Allow JARVIS: windows_system_menu?",detail=f"{r}. Waiting for your confirmation.",run=lambda:windows_system_menu(p,_permission_token=True))
 pyautogui.hotkey("alt","space")
 return "Foreground window system menu opened."
TOOL={"name":"windows_system_menu","description":"Open the standard Alt+Space system menu of the foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_system_menu}