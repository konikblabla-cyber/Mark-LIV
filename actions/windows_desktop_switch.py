"""Switch Windows virtual desktops using normal keyboard shortcuts."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_desktop_switch(parameters=None,**kwargs):
 p=parameters or {}; direction=str(p.get("direction","right")).lower()
 if direction not in ("left","right"): return "Direction must be left or right."
 pyautogui.hotkey("win","ctrl","right" if direction=="right" else "left")
 return f"Switched virtual desktop {direction}."
TOOL={"name":"windows_desktop_switch","description":"Switch Windows virtual desktops left or right using Win+Ctrl+Arrow.","parameters":{"type":"OBJECT","properties":{"direction":{"type":"STRING"}}},"handler":windows_desktop_switch}
