"""Windows workflow mouse primitive."""
import platform,time,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_workflow_click(parameters=None,**kwargs):
 p=parameters or {}; 
 try:x=int(p["x"]);y=int(p["y"])
 except (KeyError,TypeError,ValueError):return "Missing valid x/y."
 if not (0<=x<=10000 and 0<=y<=10000):return "Coordinates out of bounds."
 button=str(p.get("button","left")).lower()
 if button not in ("left","right","middle"):return "Invalid mouse button."
 pyautogui.click(x,y,button=button);time.sleep(max(0,min(float(p.get("delay",0.15)),3)))
 return f"Clicked {button} at ({x},{y})."
TOOL={"name":"windows_workflow_click","description":"Click a screen coordinate as one bounded Windows workflow step.","parameters":{"type":"OBJECT","properties":{"x":{"type":"INTEGER"},"y":{"type":"INTEGER"},"button":{"type":"STRING"},"delay":{"type":"NUMBER"}},"required":["x","y"]},"handler":windows_workflow_click}
