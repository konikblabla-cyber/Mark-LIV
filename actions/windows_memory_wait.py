"""Wait for Windows available memory to exceed a threshold."""
import platform,time,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_memory_wait(parameters=None,**kwargs):
 p=parameters or {};minimum=max(128,min(float(p.get("minimum_mb",1024)),1048576));timeout=max(1,min(int(p.get("timeout",60)),300));end=time.time()+timeout
 while time.time()<end:
  free=psutil.virtual_memory().available/1048576
  if free>=minimum:return f"Available memory: {free:.0f} MB >= {minimum:.0f} MB."
  time.sleep(1)
 return f"Available memory stayed below {minimum:.0f} MB for {timeout}s."
TOOL={"name":"windows_memory_wait","description":"Wait until Windows available RAM reaches a minimum threshold; read-only.","parameters":{"type":"OBJECT","properties":{"minimum_mb":{"type":"NUMBER"},"timeout":{"type":"INTEGER"}}},"handler":windows_memory_wait}
