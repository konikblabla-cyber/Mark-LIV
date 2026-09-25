"""Windows performance snapshot."""
import platform,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_performance_snapshot(parameters=None,**kwargs):
 cpu=psutil.cpu_percent(interval=.5); mem=psutil.virtual_memory(); io=psutil.disk_io_counters()
 return f"CPU={cpu:.1f}%\nRAM={mem.percent:.1f}% ({mem.available//(1024**2)} MB free)\nDisk read={io.read_bytes//(1024**2)} MB\nDisk write={io.write_bytes//(1024**2)} MB"
TOOL={"name":"windows_performance_snapshot","description":"Read-only Windows CPU, RAM and cumulative disk I/O performance snapshot.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_performance_snapshot}
