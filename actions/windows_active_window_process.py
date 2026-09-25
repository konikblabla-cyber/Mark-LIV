"""Read-only foreground Windows process identity."""
import platform,ctypes,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_active_window_process(parameters=None,**kwargs):
 u=ctypes.windll.user32;h=u.GetForegroundWindow();pid=ctypes.c_ulong();u.GetWindowThreadProcessId(h,ctypes.byref(pid))
 try:
  p=psutil.Process(pid.value);return f"Foreground process: {p.name()} PID={p.pid} path={p.exe()}"
 except Exception:return f"Foreground PID={pid.value}."
TOOL={"name":"windows_active_window_process","description":"Read-only identity and executable path of the process owning the foreground window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_active_window_process}
