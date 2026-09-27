"""Windows workflow mouse primitive."""
import platform,time,pyautogui
from core.permissions import permission_decision
from core import confirm
_TOKEN = object()
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_workflow_click(parameters=None,**kwargs):
 if kwargs.get("_permission_token") is not _TOKEN:
  p=dict(parameters or {})
  decision,reason=permission_decision("windows_workflow_click",p)
  if decision=="deny": return f"Permission denied: {reason}"
  if decision=="confirm":
   if confirm.pending_title(): return "There is already a confirmation waiting. Ask the user to answer it first."
   return confirm.request(key="windows_workflow_click",title="Allow JARVIS: windows_workflow_click?",detail=f"{reason}. JARVIS will wait for your confirmation before executing it.",run=lambda: windows_workflow_click(p,_permission_token=_TOKEN))
 p=parameters or {}; 
 try:x=int(p["x"]);y=int(p["y"])
 except (KeyError,TypeError,ValueError):return "Missing valid x/y."
 if not (0<=x<=10000 and 0<=y<=10000):return "Coordinates out of bounds."
 button=str(p.get("button","left")).lower()
 if button not in ("left","right","middle"):return "Invalid mouse button."
 pyautogui.click(x,y,button=button);time.sleep(max(0,min(float(p.get("delay",0.15)),3)))
 return f"Clicked {button} at ({x},{y})."
TOOL={"name":"windows_workflow_click","description":"Click a screen coordinate as one bounded Windows workflow step.","parameters":{"type":"OBJECT","properties":{"x":{"type":"INTEGER"},"y":{"type":"INTEGER"},"button":{"type":"STRING"},"delay":{"type":"NUMBER"}},"required":["x","y"]},"handler":windows_workflow_click}
