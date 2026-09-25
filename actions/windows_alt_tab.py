"""Use the normal Windows task switcher."""
import platform,pyautogui
def windows_alt_tab(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; direction=str(p.get("direction","next")).lower()
 if direction=="next": pyautogui.hotkey("alt","tab")
 elif direction=="previous": pyautogui.hotkey("alt","shift","tab")
 else:return "Direction must be next or previous."
 return f"Task switcher: {direction}."
TOOL={"name":"windows_alt_tab","description":"Switch to the next or previous Windows application using normal Alt+Tab shortcuts.","parameters":{"type":"OBJECT","properties":{"direction":{"type":"STRING"}}},"handler":windows_alt_tab}
