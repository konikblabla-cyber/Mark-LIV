"""Wait for Windows CPU usage to fall below a threshold."""
import platform,time,psutil
def windows_cpu_wait(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}
 try: threshold=max(1,min(float(p.get("below",50)),100)); timeout=max(1,min(int(p.get("timeout",30)),300))
 except (TypeError,ValueError): return "Invalid CPU threshold or timeout."
 end=time.time()+timeout;psutil.cpu_percent(None)
 while time.time()<end:
  v=psutil.cpu_percent(1)
  if v<threshold:return f"CPU usage below threshold: {v:.1f}% < {threshold:.1f}%."
 return f"CPU usage did not fall below {threshold:.1f}% within {timeout}s."
TOOL={"name":"windows_cpu_wait","description":"Wait until total Windows CPU utilization falls below a bounded percentage; read-only.","parameters":{"type":"OBJECT","properties":{"below":{"type":"NUMBER"},"timeout":{"type":"INTEGER"}}},"handler":windows_cpu_wait}
