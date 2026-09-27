"""Windows workflow text-entry primitive."""
import platform,time,pyautogui
from core.permissions import permission_decision
from core import confirm
_TOKEN = object()
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_workflow_type(parameters=None,**kwargs):
 if kwargs.get("_permission_token") is not _TOKEN:
  p=dict(parameters or {})
  decision,reason=permission_decision("windows_workflow_type",p)
  if decision=="deny": return f"Permission denied: {reason}"
  if decision=="confirm":
   if confirm.pending_title(): return "There is already a confirmation waiting. Ask the user to answer it first."
   return confirm.request(key="windows_workflow_type",title="Allow JARVIS: windows_workflow_type?",detail=f"{reason}. JARVIS will wait for your confirmation before executing it.",run=lambda: windows_workflow_type(p,_permission_token=_TOKEN))
 p=parameters or {}; text=str(p.get("text") or "")
 if len(text)>2000:return "Text too long; maximum is 2000 characters."
 pyautogui.write(text,interval=max(0,min(float(p.get("interval",0.01)),0.2)));time.sleep(max(0,min(float(p.get("delay",0.15)),3)))
 return f"Typed {len(text)} characters."
TOOL={"name":"windows_workflow_type","description":"Type bounded text into the currently focused Windows control as one workflow step.","parameters":{"type":"OBJECT","properties":{"text":{"type":"STRING"},"interval":{"type":"NUMBER"},"delay":{"type":"NUMBER"}},"required":["text"]},"handler":windows_workflow_type}
