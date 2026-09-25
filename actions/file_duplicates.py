"""Windows duplicate-file finder using size and SHA-256."""
import platform,hashlib,os
from pathlib import Path
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def file_duplicates(parameters=None,**kwargs):
 p=parameters or {}; root=Path(str(p.get("path","."))); max_files=max(1,min(int(p.get("max_files",2000)),10000))
 if not root.is_dir():return "Folder not found."
 by_size={}; seen=0
 for f in root.rglob("*"):
  if seen>=max_files:break
  try:
   if f.is_file():by_size.setdefault(f.stat().st_size,[]).append(f);seen+=1
  except OSError:pass
 groups=[]
 for size,files in by_size.items():
  if len(files)<2:continue
  hashes={}
  for f in files:
   try:
    h=hashlib.sha256()
    with f.open("rb") as x:
     for chunk in iter(lambda:x.read(1024*1024),b""):h.update(chunk)
    hashes.setdefault(h.hexdigest(),[]).append(str(f))
   except OSError:pass
  for same in hashes.values():
   if len(same)>1:groups.append(same)
 return "\n\n".join("\n".join(g) for g in groups[:100]) or "No duplicate files found."
TOOL={"name":"file_duplicates","description":"Read-only Windows duplicate-file finder using size and SHA-256; bounded scan.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"max_files":{"type":"INTEGER"}},"required":["path"]},"handler":file_duplicates}
