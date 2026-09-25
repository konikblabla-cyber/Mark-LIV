"""Bounded Windows workflow condition checks."""
import ctypes,platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def _title():
 u=ctypes.windll.user32;h=u.GetForegroundWindow();n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1);return b.value
def windows_workflow_condition(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("window_contains") or "").strip().lower(); timeout=max(0,min(int(p.get("timeout",10)),60))
 if not needle:return "Missing window_contains."
 end=time.time()+timeout
 while time.time()<end:
  t=_title()
  if needle in t.lower():return f"Condition met: active window contains '{needle}'."
  time.sleep(.25)
 return f"Condition not met within {timeout}s; active window='{_title()}'."
TOOL={"name":"windows_workflow_condition","description":"Bounded condition check for screen workflows: wait until the active Windows window title contains expected text.","parameters":{"type":"OBJECT","properties":{"window_contains":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["window_contains"]},"handler":windows_workflow_condition}
