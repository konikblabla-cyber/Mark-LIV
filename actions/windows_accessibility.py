"""Windows accessibility tools."""
import platform,subprocess
from core.permissions import permission_decision
from core import confirm
def windows_accessibility(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; action=str(p.get("action","")).lower()
 commands={"magnifier":"magnify.exe","keyboard":"osk.exe","narrator":"narrator.exe"}
 if action not in commands:return "Action must be magnifier, keyboard, or narrator."
 if not kwargs.get("_permission_token"):
  decision,reason=permission_decision("windows_accessibility",p)
  if decision=="deny":return f"Permission denied: {reason}"
  if decision=="confirm":return confirm.request(key="windows_accessibility",title="Allow JARVIS: windows_accessibility?",detail=f"{reason}. Waiting for your confirmation.",run=lambda:windows_accessibility(p,_permission_token=True))
 try:
  subprocess.Popen([commands[action]],creationflags=subprocess.CREATE_NO_WINDOW)
 except OSError as e:return f"Failed to start accessibility tool: {e}"
 return f"Started Windows accessibility tool: {action}."
TOOL={"name":"windows_accessibility","description":"Start built-in Windows Magnifier, On-Screen Keyboard, or Narrator.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_accessibility}
