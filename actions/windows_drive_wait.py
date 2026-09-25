"""Wait for a Windows drive or path to become available."""
import platform,time,os
def windows_drive_wait(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {};path=str(p.get("path") or p.get("drive") or "").strip();timeout=max(1,min(int(p.get("timeout",30)),300))
 if not path:return "Drive or path is required."
 end=time.time()+timeout
 while time.time()<end:
  if os.path.exists(path):return f"Path available: {path}"
  time.sleep(.5)
 return f"Path unavailable after {timeout}s: {path}"
TOOL={"name":"windows_drive_wait","description":"Wait for a Windows drive, network path, or other filesystem path to become available.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"drive":{"type":"STRING"},"timeout":{"type":"INTEGER"}}},"handler":windows_drive_wait}
