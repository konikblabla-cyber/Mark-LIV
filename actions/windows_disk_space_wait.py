"""Wait for Windows disk free space to exceed a threshold."""
import platform,time,shutil
def windows_disk_space_wait(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {};path=str(p.get("path") or p.get("drive") or "C:\\").strip();minimum=max(0,min(float(p.get("minimum_gb",5)),100000));timeout=max(1,min(int(p.get("timeout",60)),300));end=time.time()+timeout
 while time.time()<end:
  try:free=shutil.disk_usage(path).free/1073741824
  except OSError as e:return f"Cannot inspect disk: {e}"
  if free>=minimum:return f"Free space on {path}: {free:.1f} GB >= {minimum:.1f} GB."
  time.sleep(1)
 return f"Free space on {path} stayed below {minimum:.1f} GB for {timeout}s."
TOOL={"name":"windows_disk_space_wait","description":"Wait until a Windows filesystem path has at least a requested amount of free disk space; read-only.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"drive":{"type":"STRING"},"minimum_gb":{"type":"NUMBER"},"timeout":{"type":"INTEGER"}}},"handler":windows_disk_space_wait}
