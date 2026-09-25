"""Wait for a window title then type text."""
import platform,time,ctypes,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_wait_then_text(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("window") or "").strip().lower(); value=str(p.get("text") or ""); timeout=max(1,min(int(p.get("timeout",30)),120))
 if not needle:return "Window text is required."
 u=ctypes.windll.user32;end=time.time()+timeout
 while time.time()<end:
  h=u.GetForegroundWindow();n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
  if needle in b.value.lower():
   pyautogui.write(value,interval=0.01);return f"Window matched and text entered ({len(value)} chars)."
  time.sleep(.25)
 return f"Window not matched within {timeout}s."
TOOL={"name":"windows_wait_then_text","description":"Wait for a matching foreground Windows window and type bounded text into its focused control.","parameters":{"type":"OBJECT","properties":{"window":{"type":"STRING"},"text":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["window","text"]},"handler":windows_wait_then_text}
