"""Read-only Windows screen metrics."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_screen_info(parameters=None,**kwargs):
 u=ctypes.windll.user32
 w=u.GetSystemMetrics(0);h=u.GetSystemMetrics(1);cx=u.GetSystemMetrics(78);cy=u.GetSystemMetrics(79)
 return f"Primary screen: {w}x{h}; virtual desktop: {cx}x{cy}."
TOOL={"name":"windows_screen_info","description":"Read-only Windows primary and virtual desktop screen dimensions.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_screen_info}
