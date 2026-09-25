"""Request an application window close and wait for its process to exit."""
import ctypes,platform,time,psutil
def windows_app_close_wait(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; name=str(p.get("process") or "").strip().lower(); timeout=max(1,min(int(p.get("timeout",20)),120))
 if not name:return "Missing process name."
 targets=[x for x in psutil.process_iter(["name","pid"]) if (x.info["name"] or "").lower()==name]
 if len(targets)!=1:return f"Expected exactly one matching process, found {len(targets)}."
 proc=targets[0]; pid=proc.info["pid"]; u=ctypes.windll.user32; hwnds=[]
 def cb(hwnd,lparam):
  q=ctypes.c_ulong();u.GetWindowThreadProcessId(hwnd,ctypes.byref(q))
  if q.value==pid and u.IsWindowVisible(hwnd):hwnds.append(hwnd)
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 if not hwnds:return f"No visible window for {name}."
 for h in hwnds:u.PostMessageW(h,0x0010,0,0)
 try:proc.wait(timeout=timeout);return f"Application exited: {name} (PID {pid})."
 except psutil.TimeoutExpired:return f"Close requested, but {name} did not exit within {timeout}s."
TOOL={"name":"windows_app_close_wait","description":"Request graceful close of a uniquely matched Windows application and wait for its process to exit.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["process"]},"handler":windows_app_close_wait}
