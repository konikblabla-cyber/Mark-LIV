"""Useful normal Windows hotkeys."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
HOTKEYS={"task_view":("win","tab"),"search":("win","s"),"settings":("win","i"),"run":("win","r"),"file_explorer":("win","e")}
def windows_hotkey_action(parameters=None,**kwargs):
 p=parameters or {};action=str(p.get("action","")).lower()
 if action not in HOTKEYS:return "Unknown action. Use task_view, search, settings, run, or file_explorer."
 pyautogui.hotkey(*HOTKEYS[action]);return f"Hotkey action executed: {action}."
TOOL={"name":"windows_hotkey_action","description":"Open common Windows interfaces using their normal keyboard shortcuts.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}}},"handler":windows_hotkey_action}
