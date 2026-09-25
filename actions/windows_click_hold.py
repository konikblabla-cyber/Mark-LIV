"""Bounded Windows mouse hold action."""
import platform,time,pyautogui
def windows_click_hold(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}
 try: x=int(p.get("x",0)); y=int(p.get("y",0)); duration=max(.05,min(float(p.get("duration",.5)),10))
 except (TypeError,ValueError): return "Invalid coordinates or duration."
 button=str(p.get("button","left")).lower()
 if button not in ("left","right","middle"): return "Button must be left, right, or middle."
 pyautogui.moveTo(x,y);pyautogui.mouseDown(button=button);time.sleep(duration);pyautogui.mouseUp(button=button)
 return f"Held {button} mouse button at ({x},{y}) for {duration:.2f}s."
TOOL={"name":"windows_click_hold","description":"Move to coordinates and hold a Windows mouse button for a bounded duration.","parameters":{"type":"OBJECT","properties":{"x":{"type":"INTEGER"},"y":{"type":"INTEGER"},"button":{"type":"STRING"},"duration":{"type":"NUMBER"}},"required":["x","y"]},"handler":windows_click_hold}
