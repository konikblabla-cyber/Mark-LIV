"""Show Windows desktop."""
import platform,pyautogui
from core.permissions import permission_decision
from core import confirm
def windows_desktop_show(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 if not kwargs.get("_permission_token"):
  decision,reason=permission_decision("windows_desktop_show",parameters or {})
  if decision=="deny":return f"Permission denied: {reason}"
  if decision=="confirm":return confirm.request(key="windows_desktop_show",title="Allow JARVIS: windows_desktop_show?",detail=f"{reason}. Waiting for your confirmation.",run=lambda:windows_desktop_show(parameters or {},_permission_token=True))
 pyautogui.hotkey("win","d")
 return "Windows desktop shown."
TOOL={"name":"windows_desktop_show","description":"Show or restore the Windows desktop using Win+D.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_desktop_show}
