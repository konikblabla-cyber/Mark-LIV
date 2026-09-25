"""Read-only visibility/enabled state of the foreground Windows window."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_active_window_visibility(parameters=None,**kwargs):
 u=ctypes.windll.user32;h=u.GetForegroundWindow()
 return f"Visible={bool(u.IsWindowVisible(h))}; enabled={bool(u.IsWindowEnabled(h))}; minimized={bool(u.IsIconic(h))}."
TOOL={"name":"windows_active_window_visibility","description":"Read-only visibility, enabled and minimized state of the foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_active_window_visibility}
