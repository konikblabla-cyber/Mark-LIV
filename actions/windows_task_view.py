"""Open Windows Task View."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_task_view(parameters=None,**kwargs):
 pyautogui.hotkey("win","tab")
 return "Windows Task View opened."
TOOL={"name":"windows_task_view","description":"Open Windows Task View using the normal Win+Tab shortcut.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_task_view}
