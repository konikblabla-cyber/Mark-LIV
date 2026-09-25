"""Read-only detailed foreground UI identity."""
import ctypes,platform,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_foreground(parameters=None,**kwargs):
 u=ctypes.windll.user32; h=u.GetForegroundWindow(); pid=ctypes.c_ulong();u.GetWindowThreadProcessId(h,ctypes.byref(pid))
 n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
 try: proc=psutil.Process(pid.value); name=proc.name()
 except Exception: name="<unknown>"
 return f"Foreground: title='{b.value}', PID={pid.value}, process='{name}', HWND={h}."
TOOL={"name":"windows_ui_foreground","description":"Read-only detailed identity of the current foreground Windows window and process.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_ui_foreground}
