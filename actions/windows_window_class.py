"""Read-only Windows foreground window class."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_class(parameters=None,**kwargs):
 u=ctypes.windll.user32;h=u.GetForegroundWindow();b=ctypes.create_unicode_buffer(256);u.GetClassNameW(h,b,256)
 return f"Foreground window class: {b.value or '<unknown>'}."
TOOL={"name":"windows_window_class","description":"Read-only class name of the foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_window_class}
