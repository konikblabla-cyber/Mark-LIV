"""Bounded Windows workflow delay."""
import platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_wait_seconds(parameters=None,**kwargs):
 p=parameters or {}
 try:s=float(p.get("seconds",1))
 except Exception:return "Seconds must be numeric."
 s=max(0.1,min(s,30))
 time.sleep(s)
 return f"Waited {s:.1f}s."
TOOL={"name":"windows_wait_seconds","description":"Pause a Windows automation workflow for a bounded number of seconds.","parameters":{"type":"OBJECT","properties":{"seconds":{"type":"NUMBER"}}},"handler":windows_wait_seconds}
