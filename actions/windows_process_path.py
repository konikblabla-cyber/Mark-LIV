"""Read executable path for a Windows process."""
import platform,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_path(parameters=None,**kwargs):
 p=parameters or {}; pid=int(p.get("pid",0))
 try:
  x=psutil.Process(pid); return f"PID {pid}: {x.exe()}"
 except (ValueError,psutil.NoSuchProcess,psutil.AccessDenied) as e:return f"Cannot read process path: {e}"
TOOL={"name":"windows_process_path","description":"Read the executable path of a Windows process by PID.","parameters":{"type":"OBJECT","properties":{"pid":{"type":"INTEGER"}},"required":["pid"]},"handler":windows_process_path}
