"""Toggle Windows desktop visibility."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_desktop_toggle(parameters=None,**kwargs):
 pyautogui.hotkey("win","d")
 return "Toggled Windows desktop visibility."
TOOL={"name":"windows_desktop_toggle","description":"Toggle showing the Windows desktop with normal Win+D input.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_desktop_toggle}
