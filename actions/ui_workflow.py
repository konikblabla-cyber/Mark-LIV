"""Bounded multi-step Windows UI workflows for Mark-LIV."""
import platform, time
if platform.system() != "Windows":
    raise RuntimeError("Mark-LIV UI workflows are Windows-only.")

def ui_workflow(parameters=None, response=None, player=None, session_memory=None):
    p=parameters or {}
    steps=p.get("steps") or []
    if not isinstance(steps,list) or not steps: return "Workflow needs a non-empty steps list."
    if len(steps)>30: return "Workflow limited to 30 steps."
    from actions.computer_control import computer_control
    results=[]
    for i,step in enumerate(steps,1):
        if not isinstance(step,dict): return f"Step {i} must be an object."
        action=str(step.get("action","")).strip()
        if not action: return f"Step {i} has no action."
        result=computer_control(step,response=response,player=player,session_memory=session_memory)
        results.append(f"{i}. {result}")
        if step.get("stop_if_not_found") and ("NOT_FOUND" in result or "not found" in result.lower() or "timed out" in result.lower()):
            break
        pause=max(0.0,min(float(step.get("pause",0.2)),5.0))
        if pause: time.sleep(pause)
    return "\n".join(results)

TOOL={"name":"ui_workflow","description":"Windows-only bounded multi-step UI automation. Execute up to 30 computer actions as one task, optionally pausing and stopping when a screen element is not found. Designed for observe -> act -> observe workflows; does not bypass MFA, CAPTCHA, UAC, or security prompts.","parameters":{"type":"OBJECT","properties":{"steps":{"type":"ARRAY","description":"Ordered computer_control action objects. Each can include pause and stop_if_not_found."}},"required":["steps"]},"handler":ui_workflow}
