"""Type normal text and verify the focused foreground window."""
import platform,time,pyautogui,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_type_verify(parameters=None,**kwargs):
 p=parameters or {};text=str(p.get("text",""))
 if not text:return "Text is required."
 pyautogui.write(text,interval=0.01);time.sleep(.15)
 u=ctypes.windll.user32;h=u.GetForegroundWindow();n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
 return f"Typed {len(text)} characters; foreground window: {b.value or '<untitled>'}."
TOOL={"name":"windows_type_verify","description":"Type normal text into the focused Windows control and report the active window afterward.","parameters":{"type":"OBJECT","properties":{"text":{"type":"STRING"}},"required":["text"]},"handler":windows_type_verify}
