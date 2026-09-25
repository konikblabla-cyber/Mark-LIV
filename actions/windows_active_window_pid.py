"""Read-only PID of the foreground Windows window."""
import ctypes,platform
def windows_active_window_pid(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 u=ctypes.windll.user32;h=u.GetForegroundWindow();pid=ctypes.c_ulong();u.GetWindowThreadProcessId(h,ctypes.byref(pid))
 return f"Foreground PID: {pid.value}."
TOOL={"name":"windows_active_window_pid","description":"Read-only PID of the current foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_active_window_pid}
