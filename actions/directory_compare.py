"""Windows directory comparison by relative file paths and metadata."""
import platform
from pathlib import Path
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def directory_compare(parameters=None,**kwargs):
 p=parameters or {}; a=Path(str(p.get("left","."))); b=Path(str(p.get("right",".")))
 if not a.is_dir() or not b.is_dir():return "Both directories must exist."
 def snap(root):
  d={}
  for f in root.rglob("*"):
   if f.is_file():
    try:d[str(f.relative_to(root))]=(f.stat().st_size,f.stat().st_mtime_ns)
    except OSError:pass
  return d
 x,y=snap(a),snap(b); added=sorted(set(y)-set(x));removed=sorted(set(x)-set(y));changed=sorted(k for k in set(x)&set(y) if x[k]!=y[k])
 return f"Only left: {len(removed)}\nOnly right: {len(added)}\nChanged: {len(changed)}\n\n"+("\n".join(changed[:100]) or "No differing common files.")
TOOL={"name":"directory_compare","description":"Read-only Windows comparison of two directories by relative paths, sizes and modification times.","parameters":{"type":"OBJECT","properties":{"left":{"type":"STRING"},"right":{"type":"STRING"}},"required":["left","right"]},"handler":directory_compare}
