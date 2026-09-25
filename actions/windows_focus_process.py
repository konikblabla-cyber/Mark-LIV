"""Focus a unique visible window belonging to a process."""
import ctypes,platform,psutil

def windows_focus_process(parameters=None,**kwargs):
    if platform.system() != "Windows":
        return "windows_focus_process is Windows-only."
 p=parameters or {}; target=str(p.get("process") or "").strip().lower()
 if not target:return "Missing process name."
 u=ctypes.windll.user32; matches=[]
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long)
 def cb(hwnd,lparam):
  if not u.IsWindowVisible(hwnd): return True
  pid=ctypes.c_ulong();u.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
  try:
   if (psutil.Process(pid.value).name() or "").lower()==target:
    n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
    if b.value: matches.append((hwnd,b.value))
  except (psutil.NoSuchProcess,psutil.AccessDenied): pass
  return True
 u.EnumWindows(W(cb),0)
 if len(matches)!=1:return f"Expected exactly one titled window for {target}, found {len(matches)}."
 hwnd,title=matches[0];u.ShowWindow(hwnd,9);u.SetForegroundWindow(hwnd)
 return f"Focused {target}: '{title}'."
TOOL={"name":"windows_focus_process","description":"Focus a unique visible titled window belonging to a named Windows process.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"}},"required":["process"]},"handler":windows_focus_process}
