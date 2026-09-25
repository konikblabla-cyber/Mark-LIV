"""Short Windows CPU history sampler."""
import platform,psutil,time
def windows_cpu_history(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}
 try: seconds=max(1,min(int(p.get("seconds",10)),30)); interval=max(.5,min(float(p.get("interval",1)),5))
 except (TypeError,ValueError): return "Invalid sampling parameters."
 rows=[]; end=time.time()+seconds
 while time.time()<end:
  rows.append(f"{time.strftime('%H:%M:%S')} CPU {psutil.cpu_percent(interval=interval):.1f}%")
 return "\n".join(rows)
TOOL={"name":"windows_cpu_history","description":"Read-only short CPU utilization history for Windows.","parameters":{"type":"OBJECT","properties":{"seconds":{"type":"INTEGER"},"interval":{"type":"NUMBER"}}},"handler":windows_cpu_history}
