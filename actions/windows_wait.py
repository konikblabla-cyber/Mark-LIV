"""Bounded Windows workflow delay."""
import platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_wait(parameters=None,**kwargs):
 p=parameters or {}
 try: seconds=float(p.get("seconds",1))
 except Exception: seconds=1
 seconds=max(.05,min(seconds,30));time.sleep(seconds)
 return f"Waited {seconds:g} seconds."
TOOL={"name":"windows_wait","description":"Pause a Windows workflow for a bounded amount of time.","parameters":{"type":"OBJECT","properties":{"seconds":{"type":"NUMBER"}}},"handler":windows_wait}
