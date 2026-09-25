"""Wait for a foreground Windows window to reach a requested state."""
import ctypes,platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_state_wait(parameters=None,**kwargs):
 p=parameters or {}; wanted=str(p.get("state","visible")).lower(); timeout=max(1,min(int(p.get("timeout",20)),120));u=ctypes.windll.user32;end=time.time()+timeout
 while time.time()<end:
  h=u.GetForegroundWindow()
  ok={"visible":bool(u.IsWindowVisible(h)),"enabled":bool(u.IsWindowEnabled(h)),"minimized":bool(u.IsIconic(h)),"maximized":bool(u.IsZoomed(h))}.get(wanted)
  if ok is True:return f"Foreground window reached state: {wanted}."
  time.sleep(.25)
 return f"Foreground window did not reach state '{wanted}' within {timeout}s."
TOOL={"name":"windows_window_state_wait","description":"Wait until the foreground Windows window is visible, enabled, minimized, or maximized.","parameters":{"type":"OBJECT","properties":{"state":{"type":"STRING"},"timeout":{"type":"INTEGER"}}},"handler":windows_window_state_wait}
