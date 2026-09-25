"""Windows process resource ranking."""
import platform,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_resource_top(parameters=None,**kwargs):
 p=parameters or {}; limit=max(1,min(int(p.get("limit",15)),30))
 rows=[]
 for x in psutil.process_iter(["pid","name","memory_info"]):
  try: rows.append((x.info["memory_info"].rss if x.info["memory_info"] else 0,x.info["pid"],x.info["name"] or "unknown"))
  except (psutil.NoSuchProcess,psutil.AccessDenied): pass
 rows.sort(reverse=True)
 return "\n".join(f"{n/1048576:.1f} MB\tPID {pid}\t{name}" for n,pid,name in rows[:limit])
TOOL={"name":"windows_process_resource_top","description":"Read-only ranking of Windows processes by resident memory usage.","parameters":{"type":"OBJECT","properties":{"limit":{"type":"INTEGER"}}},"handler":windows_process_resource_top}
