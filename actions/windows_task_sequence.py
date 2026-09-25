"""Bounded sequence of existing Mark-LIV actions."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_task_sequence(parameters=None,response=None,player=None,session_memory=None):
 p=parameters or {}; tasks=p.get("tasks") or []
 if not isinstance(tasks,list) or not tasks:return "Task sequence needs tasks."
 if len(tasks)>15:return "Task sequence limited to 15 actions."
 from core.action_loader import dispatch_action
 out=[]
 for i,t in enumerate(tasks,1):
  if not isinstance(t,dict): return f"Task {i} must be an object."
  name=str(t.get("action") or "").strip()
  if not name:return f"Task {i} has no action."
  params=t.get("parameters") or {}
  try:r=dispatch_action(name,params,response=response,player=player,session_memory=session_memory)
  except Exception as e:r=f"ERROR: {e}"
  out.append(f"{i}. {name}: {r}")
  if str(r).startswith("ERROR:"):break
 return "\n".join(out)
TOOL={"name":"windows_task_sequence","description":"Execute up to 15 existing Mark-LIV actions sequentially as one bounded Windows task.","parameters":{"type":"OBJECT","properties":{"tasks":{"type":"ARRAY"}},"required":["tasks"]},"handler":windows_task_sequence}
