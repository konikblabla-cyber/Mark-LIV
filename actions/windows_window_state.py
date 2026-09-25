"""Read-only state of the foreground Windows window."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_state(parameters=None,**kwargs):
 u=ctypes.windll.user32; h=u.GetForegroundWindow()
 if not h:return "No foreground window."
 return f"HWND={h}; minimized={bool(u.IsIconic(h))}; maximized={bool(u.IsZoomed(h))}; visible={bool(u.IsWindowVisible(h))}; enabled={bool(u.IsWindowEnabled(h))}."
TOOL={"name":"windows_window_state","description":"Read-only minimized, maximized, visible and enabled state of the foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_window_state}
