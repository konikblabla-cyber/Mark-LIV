"""Wait for a Windows directory to appear."""
import platform,time,os
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_directory_wait(parameters=None,**kwargs):
 p=parameters or {};path=str(p.get("path","")).strip();timeout=max(1,min(int(p.get("timeout",30)),300))
 if not path:return "Path is required."
 end=time.time()+timeout
 while time.time()<end:
  if os.path.isdir(path):return f"Directory found: {path}"
  time.sleep(.5)
 return f"Directory not found after {timeout}s: {path}"
TOOL={"name":"windows_directory_wait","description":"Wait up to a bounded time for a specific Windows directory to appear.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["path"]},"handler":windows_directory_wait}
