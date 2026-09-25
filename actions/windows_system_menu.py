"""Open the standard Windows system menu for the foreground window."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_system_menu(parameters=None,**kwargs):
 pyautogui.hotkey("alt","space")
 return "Foreground window system menu opened."
TOOL={"name":"windows_system_menu","description":"Open the standard Alt+Space system menu of the foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_system_menu}
