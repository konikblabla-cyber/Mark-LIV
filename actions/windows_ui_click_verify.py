"""Perform a normal click and verify foreground window state."""
import platform,time,pyautogui,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_click_verify(parameters=None,**kwargs):
 p=parameters or {}
 try:x=int(p["x"]);y=int(p["y"])
 except Exception:return "Valid x and y are required."
 pyautogui.click(x,y);time.sleep(.25)
 u=ctypes.windll.user32;h=u.GetForegroundWindow();n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
 return f"Clicked ({x},{y}); foreground window: {b.value or '<untitled>'}."
TOOL={"name":"windows_ui_click_verify","description":"Click a normal Windows screen coordinate and report the resulting foreground window.","parameters":{"type":"OBJECT","properties":{"x":{"type":"INTEGER"},"y":{"type":"INTEGER"}},"required":["x","y"]},"handler":windows_ui_click_verify}
