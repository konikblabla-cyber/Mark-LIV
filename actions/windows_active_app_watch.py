"""Bounded watcher for changes of the Windows foreground application."""
import platform,ctypes,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_active_app_watch(parameters=None,**kwargs):
 p=parameters or {}; seconds=max(.5,min(float(p.get("seconds",10)),30)); u=ctypes.windll.user32; k=ctypes.windll.kernel32; end=time.time()+seconds; last=None; rows=[]
 while time.time()<end:
  h=u.GetForegroundWindow(); t=ctypes.create_unicode_buffer(256); u.GetWindowTextW(h,t,256); pid=ctypes.c_ulong(); u.GetWindowThreadProcessId(h,ctypes.byref(pid)); key=(pid.value,t.value)
  if key!=last: rows.append(f"{pid.value}\t{t.value}"); last=key
  time.sleep(.25)
 return "\n".join(rows) if rows else "No foreground-window changes observed."
TOOL={"name":"windows_active_app_watch","description":"Watch the Windows foreground application for short bounded periods and report changes.","parameters":{"type":"OBJECT","properties":{"seconds":{"type":"NUMBER"}}},"handler":windows_active_app_watch}
