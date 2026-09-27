"""Bounded Windows mouse drag path."""
import platform,pyautogui
from core.permissions import permission_decision
from core import confirm
def windows_drag_path(parameters=None,**kwargs):

             if not kwargs.get("_permission_token"):
                 p = dict(parameters or {})
                 decision, reason = permission_decision("windows_drag_path", p)
                 if decision == "deny":
                     return f"Permission denied: {reason}"
                 if decision == "confirm":
                     return confirm.request(key="windows_drag_path", title="Allow JARVIS: windows_drag_path?", detail=f"{reason}. Waiting for your confirmation.", run=lambda: windows_drag_path(p, _permission_token=True))
    if platform.system()!="Windows": return "Windows-only action."
    p=parameters or {}; start=p.get("start");end=p.get("end")
    if not isinstance(start,list) or len(start)!=2 or not isinstance(end,list) or len(end)!=2:return "start/end must be [x,y]."
    x1,y1=map(int,start);x2,y2=map(int,end);duration=max(.1,min(float(p.get("duration",.6)),10))
    pyautogui.moveTo(x1,y1);pyautogui.dragTo(x2,y2,duration=duration,button="left")
    return f"Dragged from ({x1},{y1}) to ({x2},{y2})."
TOOL={"name":"windows_drag_path","description":"Perform a bounded left-button drag between two screen coordinates.","parameters":{"type":"OBJECT","properties":{"start":{"type":"ARRAY"},"end":{"type":"ARRAY"},"duration":{"type":"NUMBER"}},"required":["start","end"]},"handler":windows_drag_path}
