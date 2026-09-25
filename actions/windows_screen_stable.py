"""Wait until the Windows screen stops changing."""
import platform,time,hashlib
from PIL import ImageGrab
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_screen_stable(parameters=None,**kwargs):
 p=parameters or {}; stable=max(.5,min(float(p.get("stable_for",1.5)),10)); timeout=max(1,min(int(p.get("timeout",30)),120))
 end=time.time()+timeout;last=None;since=time.time()
 while time.time()<end:
  im=ImageGrab.grab(); h=hashlib.sha256(im.tobytes()).hexdigest()
  if h!=last:last=h;since=time.time()
  elif time.time()-since>=stable:return f"Screen stable for {stable:.1f}s."
  time.sleep(.25)
 return f"Screen did not become stable within {timeout}s."
TOOL={"name":"windows_screen_stable","description":"Wait until the visible Windows screen remains unchanged for a short bounded period.","parameters":{"type":"OBJECT","properties":{"stable_for":{"type":"NUMBER"},"timeout":{"type":"INTEGER"}}},"handler":windows_screen_stable}
