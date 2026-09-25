"""Bounded Windows screen observation helper."""
import platform,time
def screen_observer(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}
 try: seconds=max(.2,min(float(p.get("seconds",3)),15)); interval=max(.2,min(float(p.get("interval",1)),3))
 except (TypeError,ValueError): return "Invalid observation timing."
 from actions.computer_control import computer_control
 out=[]
 end=time.time()+seconds
 while time.time()<end:
  out.append(computer_control({"action":"screenshot"},**kwargs))
  time.sleep(interval)
 return "\n".join(out)[-12000:]
TOOL={"name":"screen_observer","description":"Windows-only bounded repeated screen observation for short autonomous UI workflows; never bypasses security prompts.","parameters":{"type":"OBJECT","properties":{"seconds":{"type":"NUMBER"},"interval":{"type":"NUMBER"}}},"handler":screen_observer}
