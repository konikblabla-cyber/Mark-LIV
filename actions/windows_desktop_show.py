"""Show Windows desktop."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_desktop_show(parameters=None,**kwargs):
 pyautogui.hotkey("win","d")
 return "Windows desktop shown."
TOOL={"name":"windows_desktop_show","description":"Show or restore the Windows desktop using Win+D.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_desktop_show}
