"""Wait for a foreground window title condition."""
import ctypes,platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_verify_wait(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("contains","")).strip().lower(); timeout=max(1,min(int(p.get("timeout",20)),60))
 if not needle:return "Missing title text."
 u=ctypes.windll.user32;end=time.time()+timeout
 while time.time()<end:
  h=u.GetForegroundWindow();n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
  if needle in b.value.lower():return f"Verified after wait: '{b.value}'."
  time.sleep(.25)
 return f"Verification timed out: {needle}"
TOOL={"name":"windows_ui_verify_wait","description":"Wait until the foreground Windows window title contains expected text.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["contains"]},"handler":windows_ui_verify_wait}
