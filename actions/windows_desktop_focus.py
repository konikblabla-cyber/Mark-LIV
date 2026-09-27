"""Focus the Windows desktop shell."""
import ctypes,platform,pyautogui
def windows_desktop_focus(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 if not kwargs.get("_permission_token"):
  decision,reason=permission_decision("windows_desktop_focus",parameters or {})
  if decision=="deny":return f"Permission denied: {reason}"
  if decision=="confirm":return confirm.request(key="windows_desktop_focus",title="Allow JARVIS: windows_desktop_focus?",detail=f"{reason}. Waiting for your confirmation.",run=lambda:windows_desktop_focus(parameters or {},_permission_token=True))
 pyautogui.hotkey("win","d")
 return "Windows desktop focused."
TOOL={"name":"windows_desktop_focus","description":"Bring the Windows desktop to the foreground using normal Win+D input.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_desktop_focus}
