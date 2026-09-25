"""Wait for Windows CPU or memory usage to fall below a threshold."""
import platform,time,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_resource_wait(parameters=None,**kwargs):
 p=parameters or {}; metric=str(p.get("metric","cpu")).lower(); threshold=float(p.get("below",50)); timeout=max(1,min(int(p.get("timeout",30)),120))
 if metric not in ("cpu","memory"):return "Metric must be cpu or memory."
 threshold=max(1,min(threshold,99)); end=time.time()+timeout
 while time.time()<end:
  value=psutil.cpu_percent(interval=.5) if metric=="cpu" else psutil.virtual_memory().percent
  if value<threshold:return f"{metric} usage is {value:.1f}%, below {threshold:.1f}%."
 return f"{metric} usage stayed at or above {threshold:.1f}% for {timeout}s."
TOOL={"name":"windows_resource_wait","description":"Wait for Windows CPU or memory utilization to fall below a threshold before continuing a task.","parameters":{"type":"OBJECT","properties":{"metric":{"type":"STRING"},"below":{"type":"NUMBER"},"timeout":{"type":"INTEGER"}}},"handler":windows_resource_wait}
