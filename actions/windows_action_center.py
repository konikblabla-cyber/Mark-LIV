"""Open Windows Quick Settings."""
import platform,pyautogui
from core.permissions import permission_decision
from core import confirm
def windows_action_center(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 if not kwargs.get("_permission_token"):
  decision,reason=permission_decision("windows_action_center",parameters or {})
  if decision=="deny":return f"Permission denied: {reason}"
  if decision=="confirm":return confirm.request(key="windows_action_center",title="Allow JARVIS: windows_action_center?",detail=f"{reason}. Waiting for your confirmation.",run=lambda:windows_action_center(parameters or {},_permission_token=True))
 pyautogui.hotkey("win","a"); return "Windows Quick Settings opened."
TOOL={"name":"windows_action_center","description":"Open Windows Quick Settings with the normal Win+A shortcut.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_action_center}
