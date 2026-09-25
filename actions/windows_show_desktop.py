"""Windows desktop show/restore shortcut."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_show_desktop(parameters=None,**kwargs):
 pyautogui.hotkey("win","d")
 return "Toggled Windows desktop visibility."
TOOL={"name":"windows_show_desktop","description":"Toggle showing or restoring the Windows desktop with the normal Win+D shortcut.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_show_desktop}
