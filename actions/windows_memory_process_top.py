"""Windows process ranking by private memory."""
import platform,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_memory_process_top(parameters=None,**kwargs):
 p=parameters or {}; limit=max(1,min(int(p.get("limit",15)),30)); rows=[]
 for x in psutil.process_iter(["pid","name"]):
  try:
   mi=x.memory_info(); rows.append((getattr(mi,"private",mi.rss),x.pid,x.info["name"] or "unknown"))
  except (psutil.NoSuchProcess,psutil.AccessDenied): pass
 rows.sort(reverse=True)
 return "\n".join(f"{n/1048576:.1f} MB\tPID {pid}\t{name}" for n,pid,name in rows[:limit])
TOOL={"name":"windows_memory_process_top","description":"Read-only Windows process ranking by private memory when available.","parameters":{"type":"OBJECT","properties":{"limit":{"type":"INTEGER"}}},"handler":windows_memory_process_top}
