"""Windows screen change detector."""
import platform,time,hashlib
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_screen_change(parameters=None,**kwargs):
 p=parameters or {}; seconds=max(.5,min(float(p.get("seconds",8)),30)); interval=max(.25,min(float(p.get("interval",1)),3))
 from actions.computer_control import computer_control
 last=None; changes=0; end=time.time()+seconds
 while time.time()<end:
  shot=computer_control({"action":"screenshot"},**kwargs); digest=hashlib.sha256(str(shot).encode()).hexdigest()
  if last is not None and digest!=last: changes+=1
  last=digest; time.sleep(interval)
 return f"Screen observation completed. Detected {changes} screenshot-output changes."
TOOL={"name":"windows_screen_change","description":"Bounded Windows screen-change detector based on repeated screenshot observations.","parameters":{"type":"OBJECT","properties":{"seconds":{"type":"NUMBER"},"interval":{"type":"NUMBER"}}},"handler":windows_screen_change}
