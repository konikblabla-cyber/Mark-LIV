"""Wait for a screen element and click it using existing screen vision."""
import platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_wait_then_click(parameters=None,**kwargs):
 p=parameters or {}; target=str(p.get("target") or "").strip(); timeout=max(1,min(int(p.get("timeout",60)),120))
 if not target:return "Target is required."
 from actions.computer_control import computer_control
 end=time.time()+timeout
 while time.time()<end:
  r=computer_control({"action":"screen_click","description":target})
  s=str(r)
  if "not found" not in s.lower() and "failed" not in s.lower():return f"Clicked: {target}"
  time.sleep(.5)
 return f"Target not found within {timeout}s: {target}"
TOOL={"name":"windows_wait_then_click","description":"Wait for a described visible screen element and click it, using existing screen recognition.","parameters":{"type":"OBJECT","properties":{"target":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["target"]},"handler":windows_wait_then_click}
