"""Bounded conditional Windows UI workflow."""
import platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_conditional_workflow(parameters=None,response=None,player=None,session_memory=None):
 p=parameters or {}; steps=p.get("steps") or []
 if not isinstance(steps,list) or not steps:return "Workflow needs steps."
 if len(steps)>30:return "Workflow limited to 30 steps."
 from actions.computer_control import computer_control
 from actions.windows_foreground_title import windows_foreground_title
 out=[]
 for i,s in enumerate(steps,1):
  if not isinstance(s,dict): return f"Step {i} must be an object."
  cond=str(s.get("if_title_contains","")).strip().lower()
  if cond and cond not in windows_foreground_title().lower(): out.append(f"{i}. skipped"); continue
  a=s.get("action")
  if not isinstance(a,str) or not a.strip(): return f"Step {i} has no action."
  out.append(f"{i}. {computer_control(s,response=response,player=player,session_memory=session_memory)}")
  time.sleep(max(0,min(float(s.get("pause",.2)),5)))
 return "\n".join(out)
TOOL={"name":"windows_conditional_workflow","description":"Windows-only bounded UI workflow that can skip steps based on the current foreground window title.","parameters":{"type":"OBJECT","properties":{"steps":{"type":"ARRAY"}},"required":["steps"]},"handler":windows_conditional_workflow}
