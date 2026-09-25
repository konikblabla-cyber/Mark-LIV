"""Navigate the focused Windows File Explorer window to a folder."""
import ctypes,platform,os,pyautogui,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_explorer_location(parameters=None,**kwargs):
 p=parameters or {}; path=os.path.abspath(os.path.expandvars(os.path.expanduser(str(p.get("path") or ""))))
 if not os.path.isdir(path): return f"Folder does not exist: {path}"
 u=ctypes.windll.user32; h=u.GetForegroundWindow(); n=u.GetWindowTextLengthW(h); b=ctypes.create_unicode_buffer(n+1); u.GetWindowTextW(h,b,n+1)
 if "explorer" not in b.value.lower(): return "Foreground window is not File Explorer."
 pyautogui.hotkey("ctrl","l"); time.sleep(.15); pyautogui.write(path,interval=0.002); pyautogui.press("enter")
 return f"Navigated File Explorer to {path}."
TOOL={"name":"windows_explorer_location","description":"Navigate the focused Windows File Explorer window to an existing folder path.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}},"required":["path"]},"handler":windows_explorer_location}
