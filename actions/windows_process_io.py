"""Windows per-process I/O snapshot."""
import platform,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_io(parameters=None,**kwargs):
 p=parameters or {}; pid=int(p.get("pid",0))
 if pid<=0:return "Valid PID is required."
 try:
  x=psutil.Process(pid); io=x.io_counters()
  return f"PID {pid} {x.name()}\nRead={io.read_bytes//1048576} MB\nWrite={io.write_bytes//1048576} MB\nOther={io.other_bytes//1048576} MB"
 except (psutil.NoSuchProcess,psutil.AccessDenied) as e:return f"Process unavailable: {e}"
TOOL={"name":"windows_process_io","description":"Read-only per-process Windows disk I/O counters for a PID.","parameters":{"type":"OBJECT","properties":{"pid":{"type":"INTEGER"}},"required":["pid"]},"handler":windows_process_io}
