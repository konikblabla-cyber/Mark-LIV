"""Windows built-in support tools."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_quick_assist(parameters=None,**kwargs):
 p=parameters or {}; action=str(p.get("action","")).lower()
 commands={"remote_assistance":"msra.exe","quick_assist":"quickassist.exe","steps_recorder":"psr.exe"}
 if action not in commands:return "Action must be remote_assistance, quick_assist, or steps_recorder."
 subprocess.Popen([commands[action]],creationflags=subprocess.CREATE_NO_WINDOW)
 return f"Started Windows support tool: {action}."
TOOL={"name":"windows_quick_assist","description":"Start built-in Windows support and troubleshooting tools.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_quick_assist}
