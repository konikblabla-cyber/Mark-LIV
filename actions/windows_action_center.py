"""Open Windows Quick Settings."""
import platform,pyautogui
def windows_action_center(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 pyautogui.hotkey("win","a"); return "Windows Quick Settings opened."
TOOL={"name":"windows_action_center","description":"Open Windows Quick Settings with the normal Win+A shortcut.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_action_center}
