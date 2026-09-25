"""Compact snapshot of current Windows UI state."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_snapshot(parameters=None,**kwargs):
 u=ctypes.windll.user32; hwnd=u.GetForegroundWindow(); n=u.GetWindowTextLengthW(hwnd)
 b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
 return f"Active window: {b.value or '<untitled>'}; screen={u.GetSystemMetrics(0)}x{u.GetSystemMetrics(1)}."
TOOL={"name":"windows_ui_snapshot","description":"Read-only compact snapshot of active Windows window and primary screen.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_ui_snapshot}
