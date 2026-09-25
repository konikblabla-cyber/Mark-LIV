"""Focus a uniquely matched Windows window by title text."""
import ctypes, platform

def windows_focus_title(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "windows_focus_title is Windows-only."
    p=parameters or {}; needle=str(p.get("contains") or "").strip().lower()
    if not needle:return "Missing title text."
    u=ctypes.windll.user32;matches=[]
    def cb(hwnd,lparam):
        if not u.IsWindowVisible(hwnd): return True
        n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
        if needle in b.value.lower():matches.append(hwnd)
        return True
    W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
    if len(matches)!=1:return f"Expected exactly one matching window; found {len(matches)}."
    u.SetForegroundWindow(matches[0]);return f"Focused window matching '{needle}'."

TOOL={"name":"windows_focus_title","description":"Focus exactly one visible Windows window matched by title text.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"}},"required":["contains"]},"handler=windows_focus_title}
