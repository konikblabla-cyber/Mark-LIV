"""Read-only Windows control-state snapshot for automation recovery."""
import ctypes,platform
def windows_control_snapshot(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 u=ctypes.windll.user32;h=u.GetForegroundWindow();n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
 return f"Window='{b.value or '<untitled>'}', minimized={bool(u.IsIconic(h))}, maximized={bool(u.IsZoomed(h))}, cursor=({u.GetCursorPos(ctypes.pointer(ctypes.wintypes.POINT())) if False else 'available'})."
TOOL={"name":"windows_control_snapshot","description":"Read-only Windows foreground control state for automation recovery.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_control_snapshot}
