"""Windows mouse drag-and-drop action."""
import platform,pyautogui,time
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_mouse_drag(parameters=None,**kwargs):
    if not kwargs.get("_permission_token"):
        p=dict(parameters or {})
        decision,reason=permission_decision("windows_mouse_drag",p)
        if decision=="deny": return f"Permission denied: {reason}"
        if decision=="confirm":
            return confirm.request(key="windows_mouse_drag",title="Allow JARVIS: windows_mouse_drag?",detail=f"{reason}. Waiting for your confirmation.",run=lambda: windows_mouse_drag(p,_permission_token=True))
    p=parameters or {}
    try:x1,y1,x2,y2=[int(p[k]) for k in ("x1","y1","x2","y2")]
    except Exception:return "Required coordinates: x1,y1,x2,y2."
    duration=max(.05,min(float(p.get("duration",.4)),3))
    pyautogui.moveTo(x1,y1,duration=.1);pyautogui.mouseDown();time.sleep(.1);pyautogui.moveTo(x2,y2,duration=duration);pyautogui.mouseUp()
    return f"Dragged from ({x1},{y1}) to ({x2},{y2})."
TOOL={"name":"windows_mouse_drag","description":"Perform a bounded normal Windows mouse drag between screen coordinates.","parameters":{"type":"OBJECT","properties":{"x1":{"type":"INTEGER"},"y1":{"type":"INTEGER"},"x2":{"type":"INTEGER"},"y2":{"type":"INTEGER"},"duration":{"type":"NUMBER"}},"required":["x1","y1","x2","y2"]},"handler":windows_mouse_drag}