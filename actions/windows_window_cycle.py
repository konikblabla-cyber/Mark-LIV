"""Cycle Windows foreground windows."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_cycle(parameters=None,**kwargs):
 d=str((parameters or {}).get("direction","next")).lower()
 if d=="next": pyautogui.hotkey("alt","tab")
 elif d=="previous": pyautogui.hotkey("alt","shift","tab")
 else:return "Direction must be next or previous."
 return f"Window cycle requested: {d}."
TOOL={"name":"windows_window_cycle","description":"Cycle between Windows windows with normal Alt+Tab input.","parameters":{"type":"OBJECT","properties":{"direction":{"type":"STRING"}}},"handler":windows_window_cycle}
