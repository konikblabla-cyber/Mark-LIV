"""Short Windows CPU history sampler."""
import platform,psutil,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_cpu_history(parameters=None,**kwargs):
 p=parameters or {}; seconds=max(1,min(int(p.get("seconds",10)),30)); interval=max(.5,min(float(p.get("interval",1)),5))
 rows=[]; end=time.time()+seconds
 while time.time()<end:
  rows.append(f"{time.strftime('%H:%M:%S')} CPU {psutil.cpu_percent(interval=interval):.1f}%")
 return "\n".join(rows)
TOOL={"name":"windows_cpu_history","description":"Read-only short CPU utilization history for Windows.","parameters":{"type":"OBJECT","properties":{"seconds":{"type":"INTEGER"},"interval":{"type":"NUMBER"}}},"handler":windows_cpu_history}
