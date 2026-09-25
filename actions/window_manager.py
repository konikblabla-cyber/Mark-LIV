"""Windows window inventory and targeted window management for Mark-LIV."""
import ctypes, platform
from ctypes import wintypes
user32=ctypes.windll.user32

def _windows():
    out=[]
    WNDENUMPROC=ctypes.WINFUNCTYPE(ctypes.c_bool,wintypes.HWND,wintypes.LPARAM)
    def cb(hwnd,_):
        if not user32.IsWindowVisible(hwnd): return True
        n=user32.GetWindowTextLengthW(hwnd)
        if n:
            b=ctypes.create_unicode_buffer(n+1); user32.GetWindowTextW(hwnd,b,n+1)
            out.append((hwnd,b.value))
        return True
    user32.EnumWindows(WNDENUMPROC(cb),0)
    return out

def window_manager(parameters=None, response=None, player=None, session_memory=None):
    if platform.system()!="Windows": return "Windows-only action."
    p=parameters or {}; a=str(p.get("action","list")).lower().strip()
    if a=="list":
        return "\n".join(f"{h}: {t}" for h,t in _windows()) or "No visible windows."
    title=str(p.get("title","")).strip().casefold()
    if not title: return "Window title is required."
    matches=[(h,t) for h,t in _windows() if title in t.casefold()]
    if not matches: return f"No visible window matching '{title}'."
    hwnd,_=matches[0]
    SW={ "minimize":6, "maximize":3, "restore":9 }.get(a)
    if SW is not None:
        user32.ShowWindow(hwnd,SW); return f"{a.title()}d window."
    if a=="focus":
        user32.ShowWindow(hwnd,9); user32.SetForegroundWindow(hwnd); return "Focused window."
    if a=="close":
        user32.PostMessageW(hwnd,0x0010,0,0); return "Close requested for window."
    return f"Unknown window action: {a}"

TOOL={"name":"window_manager","description":"Windows window manager: list visible windows and focus, minimize, maximize, restore, or request close for a window by title.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","description":"list | focus | minimize | maximize | restore | close"},"title":{"type":"STRING","description":"Window title fragment"}},"required":["action"]},"handler":window_manager}
