"""Detailed information about the current Windows foreground window."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_details(parameters=None,**kwargs):
 u=ctypes.windll.user32; k=ctypes.windll.kernel32
 hwnd=u.GetForegroundWindow()
 if not hwnd:return "No foreground window."
 title=ctypes.create_unicode_buffer(512); u.GetWindowTextW(hwnd,title,512)
 pid=ctypes.c_ulong(); u.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
 name="unknown"
 try:
  import psutil
  name=psutil.Process(pid.value).name()
 except Exception: pass
 return f"HWND={hwnd}\nPID={pid.value}\nProcess={name}\nTitle={title.value}"
TOOL={"name":"windows_window_details","description":"Read-only details of the current Windows foreground window and owning process.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_window_details}
