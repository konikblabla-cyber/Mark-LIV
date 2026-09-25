"""Bounded sequence of existing Mark-LIV actions."""
import platform,time
def windows_action_sequence(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; actions=p.get("actions",[])
 if not isinstance(actions,list) or not actions:return "Missing actions list."
 if len(actions)>20:return "Maximum 20 actions."
 dispatcher=kwargs.get("dispatch_action") or kwargs.get("dispatcher")
 if not callable(dispatcher):return "Action dispatcher unavailable."
 out=[]
 for i,a in enumerate(actions,1):
  if not isinstance(a,dict):return f"Action {i} is invalid."
  name=str(a.get("action") or "").strip()
  if not name:return f"Action {i} has no action name."
  try: out.append(f"{i}. {dispatcher(a)}")
  except Exception as e: return f"Stopped at action {i}: {e}"
  try: pause=max(0,min(float(a.get("pause",0.15)),3))
  except (TypeError,ValueError): return f"Action {i} has invalid pause."
  time.sleep(pause)
 return "\n".join(out)
TOOL={"name":"windows_action_sequence","description":"Execute up to 20 already-available Mark-LIV actions sequentially with bounded pauses.","parameters":{"type":"OBJECT","properties":{"actions":{"type":"ARRAY"}}, "required":["actions"]},"handler":windows_action_sequence}
