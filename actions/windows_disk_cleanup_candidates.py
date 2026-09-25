"""Read-only Windows cleanup candidate scanner."""
import platform,os
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_disk_cleanup_candidates(parameters=None,**kwargs):
 p=parameters or {}; roots=[Path(os.environ.get("TEMP",r"C:\Windows\Temp")),Path(r"C:\Windows\Temp")]; rows=[]
 for root in roots:
  if not root.is_dir():continue
  for base,dirs,files in os.walk(root):
   for n in files[:300]:
    q=Path(base)/n
    try:rows.append((q.stat().st_size,str(q)))
    except OSError:pass
   if len(rows)>=1000:break
  if len(rows)>=1000:break
 rows.sort(reverse=True)
 return "\n".join(f"{s/1048576:.1f} MB\t{q}" for s,q in rows[:100]) or "No cleanup candidates found."
TOOL={"name":"windows_disk_cleanup_candidates","description":"Read-only scan of Windows TEMP locations for large cleanup candidates; never deletes files.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_disk_cleanup_candidates}
