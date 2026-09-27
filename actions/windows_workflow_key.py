"""Windows workflow keyboard primitive with bounded validation."""
import platform,time,pyautogui
from core.permissions import permission_decision
from core import confirm
_TOKEN = object()
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_workflow_key(parameters=None,**kwargs):
 if kwargs.get("_permission_token") is not _TOKEN:
  p=dict(parameters or {})
  decision,reason=permission_decision("windows_workflow_key",p)
  if decision=="deny": return f"Permission denied: {reason}"
  if decision=="confirm":
   if confirm.pending_title(): return "There is already a confirmation waiting. Ask the user to answer it first."
   return confirm.request(key="windows_workflow_key",title="Allow JARVIS: windows_workflow_key?",detail=f"{reason}. JARVIS will wait for your confirmation before executing it.",run=lambda: windows_workflow_key(p,_permission_token=_TOKEN))
 p=parameters or {}; key=str(p.get("key") or "").strip().lower(); delay=max(0,min(float(p.get("delay",0.15)),3))
 if not key:return "Missing key."
 pyautogui.press(key);time.sleep(delay)
 return f"Pressed key: {key}."
TOOL={"name":"windows_workflow_key","description":"Press one normal Windows keyboard key as a workflow step.","parameters":{"type":"OBJECT","properties":{"key":{"type":"STRING"},"delay":{"type":"NUMBER"}},"required":["key"]},"handler":windows_workflow_key}
