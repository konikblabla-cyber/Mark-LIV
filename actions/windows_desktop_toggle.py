"""Toggle Windows desktop visibility."""
import platform,pyautogui
def windows_desktop_toggle(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 pyautogui.hotkey("win","d")
 return "Toggled Windows desktop visibility."
TOOL={"name":"windows_desktop_toggle","description":"Toggle showing the Windows desktop with normal Win+D input.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_desktop_toggle}
