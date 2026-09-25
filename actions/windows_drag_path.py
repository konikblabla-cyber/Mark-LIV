"""Bounded Windows mouse drag path."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_drag_path(parameters=None,**kwargs):
 p=parameters or {}; start=p.get("start");end=p.get("end")
 if not isinstance(start,list) or len(start)!=2 or not isinstance(end,list) or len(end)!=2:return "start/end must be [x,y]."
 x1,y1=map(int,start);x2,y2=map(int,end);duration=max(.1,min(float(p.get("duration",.6)),10))
 pyautogui.moveTo(x1,y1);pyautogui.dragTo(x2,y2,duration=duration,button="left")
 return f"Dragged from ({x1},{y1}) to ({x2},{y2})."
TOOL={"name":"windows_drag_path","description":"Perform a bounded left-button drag between two screen coordinates.","parameters":{"type":"OBJECT","properties":{"start":{"type":"ARRAY"},"end":{"type":"ARRAY"},"duration":{"type":"NUMBER"}},"required":["start","end"]},"handler":windows_drag_path}
