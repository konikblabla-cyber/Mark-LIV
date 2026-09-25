"""Small bounded pause for screen-driven Windows workflows."""
import platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_input_pause(parameters=None,**kwargs):
 p=parameters or {}; seconds=max(0,min(float(p.get("seconds",0.5)),10))
 time.sleep(seconds);return f"Paused {seconds:g}s."
TOOL={"name":"windows_input_pause","description":"Pause briefly between Windows UI automation steps, bounded to 10 seconds.","parameters":{"type":"OBJECT","properties":{"seconds":{"type":"NUMBER"}}},"handler":windows_input_pause}
