"""Read-only Windows file age report for a directory."""
import platform,os,time
from pathlib import Path
def windows_disk_file_age(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; root=Path(str(p.get("root","")).strip()); days=max(1,min(int(p.get("days",30)),3650))
 if not root.is_dir():return "Directory is required."
 cutoff=time.time()-days*86400; rows=[]
 for base,dirs,files in os.walk(root):
  for n in files:
   q=Path(base)/n
   try:
    st=q.stat()
    if st.st_mtime<cutoff:rows.append((st.st_mtime,st.st_size,str(q)))
   except OSError:pass
   if len(rows)>=1000:break
  if len(rows)>=1000:break
 rows.sort()
 return "\n".join(f"{time.strftime('%Y-%m-%d',time.localtime(t))}\t{s/1048576:.1f} MB\t{q}" for t,s,q in rows[:100]) or "No old files found."
TOOL={"name":"windows_disk_file_age","description":"Read-only bounded report of files older than a chosen age in a directory.","parameters":{"type":"OBJECT","properties":{"root":{"type":"STRING"},"days":{"type":"INTEGER"}},"required":["root"]},"handler":windows_disk_file_age}
