"""Bounded Windows free-space monitor."""
import platform,shutil,time
def windows_disk_space_watch(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; path=str(p.get("path","C:\\")).strip() or "C:\\"; seconds=max(1,min(int(p.get("seconds",20)),60)); interval=max(1,min(float(p.get("interval",5)),10)); rows=[]; end=time.time()+seconds
 while time.time()<end:
  try:
   total,used,free=shutil.disk_usage(path); rows.append(f"{time.strftime('%H:%M:%S')} free={free//1073741824} GB")
  except OSError as e:return f"Disk check failed: {e}"
  time.sleep(interval)
 return "\n".join(rows)
TOOL={"name":"windows_disk_space_watch","description":"Bounded read-only Windows disk free-space monitor.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"seconds":{"type":"INTEGER"},"interval":{"type":"NUMBER"}}},"handler":windows_disk_space_watch}
