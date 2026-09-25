"""Cycle taskbar application buttons."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_taskbar_cycle(parameters=None,**kwargs):
 p=parameters or {}; direction=str(p.get("direction","next")).lower()
 if direction not in ("next","previous"):return "Direction must be next or previous."
 pyautogui.hotkey("win","t");pyautogui.press("right" if direction=="next" else "left")
 return f"Moved taskbar selection {direction}."
TOOL={"name":"windows_taskbar_cycle","description":"Move selection between Windows taskbar application buttons using normal keyboard navigation.","parameters":{"type":"OBJECT","properties":{"direction":{"type":"STRING"}}},"handler":windows_taskbar_cycle}
