"""Verify the Windows foreground application."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_foreground_verify(parameters=None,**kwargs):
 p=parameters or {}; expected=str(p.get("contains") or p.get("title") or "").strip().lower()
 u=ctypes.windll.user32; hwnd=u.GetForegroundWindow(); n=u.GetWindowTextLengthW(hwnd)
 b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1); title=b.value
 if expected and expected not in title.lower(): return f"Foreground verification failed: '{title}'."
 return f"Foreground verified: '{title}'."
TOOL={"name":"windows_foreground_verify","description":"Verify expected text in the current Windows foreground window title.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"},"title":{"type":"STRING"}}},"handler":windows_foreground_verify}
