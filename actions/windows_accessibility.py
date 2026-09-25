"""Windows accessibility tools."""
import platform,subprocess
def windows_accessibility(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; action=str(p.get("action","")).lower()
 commands={"magnifier":"magnify.exe","keyboard":"osk.exe","narrator":"narrator.exe"}
 if action not in commands:return "Action must be magnifier, keyboard, or narrator."
 try:
  subprocess.Popen([commands[action]],creationflags=subprocess.CREATE_NO_WINDOW)
 except OSError as e:return f"Failed to start accessibility tool: {e}"
 return f"Started Windows accessibility tool: {action}."
TOOL={"name":"windows_accessibility","description":"Start built-in Windows Magnifier, On-Screen Keyboard, or Narrator.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_accessibility}
