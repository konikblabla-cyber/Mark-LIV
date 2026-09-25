"""Windows-only bounded directory change snapshot."""
import platform,os
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def file_watch(parameters=None,**kwargs):
 p=parameters or {}; root=Path(str(p.get("path","")).strip()).expanduser()
 if not root.is_dir():return "Directory not found."
 try:
  rows=[]
  for base,dirs,files in os.walk(root):
   dirs[:]=dirs[:100]
   for name in files[:500]:
    q=Path(base)/name
    try:rows.append((q.stat().st_mtime,q.stat().st_size,str(q)))
    except OSError:pass
    if len(rows)>=2000:break
   if len(rows)>=2000:break
  rows.sort(reverse=True)
  return "\n".join(f"{t:.3f}\t{s}\t{q}" for t,s,q in rows[:200]) or "No files found."
 except OSError as e:return f"File watch failed: {e}"
TOOL={"name":"file_watch","description":"Windows-only bounded directory snapshot sorted by modification time, useful for finding files changed recently without scanning the whole disk.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}},"required":["path"]},"handler":file_watch}
