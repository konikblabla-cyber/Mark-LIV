"""Bounded Windows UI workflow orchestration for Mark-LIV."""
import platform,time

def ui_workflow(parameters=None, response=None, player=None, session_memory=None):
    if platform.system()!="Windows": return "Windows-only action."
    p=parameters or {}; steps=p.get("steps") or []
    if not isinstance(steps,list) or not steps:return "Workflow needs a non-empty steps list."
    if len(steps)>30:return "Workflow limited to 30 steps."
    from actions.computer_control import computer_control
    results=[]; previous=""
    for i,step in enumerate(steps,1):
        if not isinstance(step,dict):return f"Step {i} must be an object."
        cond=str(step.get("if_previous_contains","")).strip().lower()
        if cond and cond not in previous.lower():
            results.append(f"{i}. skipped: previous result did not contain '{cond}'"); previous=results[-1]; continue
        wait_for=str(step.get("wait_for","")).strip()
        if wait_for:
            wr=computer_control({"action":"screen_wait_for","description":wait_for,"timeout":step.get("wait_timeout",30),"interval":step.get("wait_interval",0.8)},response=response,player=player,session_memory=session_memory)
            results.append(f"{i}. wait: {wr}")
            if "timed out" in wr.lower() or "not found" in wr.lower():
                if not step.get("continue_on_wait_timeout",False): break
        action=str(step.get("action","")).strip()
        if not action:return f"Step {i} has no action."
        try: attempts=max(1,min(int(step.get("retry",1)),5)); delay=max(0.2,min(float(step.get("retry_delay",0.8)),5.0))
        except (TypeError,ValueError): return f"Step {i} has invalid retry settings."
        result=""
        for attempt in range(1,attempts+1):
            result=computer_control(step,response=response,player=player,session_memory=session_memory)
            low=result.lower()
            if not any(x in low for x in ("failed","not found","timed out","unknown action")): break
            if attempt<attempts: time.sleep(delay)
        previous=result; results.append(f"{i}. {result}")
        low=result.lower()
        if step.get("stop_if_not_found") and ("not found" in low or "timed out" in low or "failed" in low): break
        try: pause=max(0.0,min(float(step.get("pause",0.2)),5.0))
        except (TypeError,ValueError): pause=0.2
        if pause: time.sleep(pause)
    return "\n".join(results)

TOOL={"name":"ui_workflow","description":"Windows multi-step UI orchestration with conditional steps, wait-for-screen gates, bounded retries and stop/continue controls. Uses normal input and never bypasses MFA, CAPTCHA, UAC or security prompts.","parameters":{"type":"OBJECT","properties":{"steps":{"type":"ARRAY","description":"Ordered computer_control steps. Optional: if_previous_contains, wait_for, retry, retry_delay, wait_timeout, pause, stop_if_not_found."}},"required":["steps"]},"handler":ui_workflow}
