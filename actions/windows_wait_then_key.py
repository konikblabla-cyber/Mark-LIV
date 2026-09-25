"""Wait for a window title then send a normal key sequence."""
import platform,time,ctypes,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_wait_then_key(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("window") or "").strip().lower(); keys=p.get("keys",[]); timeout=max(1,min(int(p.get("timeout",30)),120))
 if not needle or not isinstance(keys,list) or not keys:return "Window text and keys are required."
 u=ctypes.windll.user32;end=time.time()+timeout
 while time.time()<end:
  h=u.GetForegroundWindow();n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
  if needle in b.value.lower():
   for k in keys[:30]: pyautogui.press(str(k))
   return f"Window matched and sent {min(len(keys),30)} keys."
  time.sleep(.25)
 return f"Window not matched within {timeout}s."
TOOL={"name":"windows_wait_then_key","description":"Wait for matching foreground window title and then send a bounded normal key sequence.","parameters":{"type":"OBJECT","properties":{"window":{"type":"STRING"},"keys":{"type":"ARRAY","items":{"type":"STRING"}},"timeout":{"type":"INTEGER"}},"required":["window","keys"]},"handler":windows_wait_then_key}
