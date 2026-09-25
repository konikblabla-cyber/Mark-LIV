"""Show Windows desktop."""
import platform,pyautogui
def windows_desktop_show(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 pyautogui.hotkey("win","d")
 return "Windows desktop shown."
TOOL={"name":"windows_desktop_show","description":"Show or restore the Windows desktop using Win+D.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_desktop_show}
