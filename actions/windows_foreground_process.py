"""Read-only foreground Windows process details."""
import platform,ctypes,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_foreground_process(parameters=None,**kwargs):
 u=ctypes.windll.user32; hwnd=u.GetForegroundWindow(); pid=ctypes.c_ulong();u.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
 try:
  p=psutil.Process(pid.value); return f"Foreground PID={pid.value}; process={p.name()}; exe={p.exe()}"
 except (psutil.NoSuchProcess,psutil.AccessDenied): return f"Foreground PID={pid.value}; process details unavailable."
TOOL={"name":"windows_foreground_process","description":"Read-only process name and executable path owning the foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_foreground_process}
