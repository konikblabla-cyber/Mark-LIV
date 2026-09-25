"""Normal Windows virtual-desktop shortcuts."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_virtual_desktop_hotkeys(parameters=None,**kwargs):
 p=parameters or {}; action=str(p.get("action","overview")).lower()
 keys={"overview":["win","tab"],"new":["win","ctrl","d"],"close":["win","ctrl","f4"]}
 if action not in keys:return "Action must be overview, new, or close."
 pyautogui.hotkey(*keys[action])
 return f"Virtual desktop action: {action}."
TOOL={"name":"windows_virtual_desktop_hotkeys","description":"Use normal Windows shortcuts to open Task View, create a virtual desktop, or close the current virtual desktop.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}}},"handler":windows_virtual_desktop_hotkeys}
