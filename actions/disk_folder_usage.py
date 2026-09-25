"""Windows folder disk usage inspection."""
import platform,os
from pathlib import Path
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def disk_folder_usage(parameters=None,**kwargs):
 p=parameters or {}; root=Path(str(p.get("path",r"C:\Users"))); limit=max(1,min(int(p.get("limit",20)),100))
 if not root.exists() or not root.is_dir():return "Folder not found."
 rows=[]
 for child in root.iterdir():
  if not child.is_dir():continue
  total=0
  try:
   for f in child.rglob("*"):
    if f.is_file():
     try:total+=f.stat().st_size
     except OSError:pass
  except OSError:pass
  rows.append((total,str(child)))
 rows.sort(reverse=True)
 return "\n".join(f"{s/1073741824:.2f} GB\t{p}" for s,p in rows[:limit]) or "No subfolders."
TOOL={"name":"disk_folder_usage","description":"Read-only Windows folder usage report showing which immediate subfolders consume the most disk space.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"limit":{"type":"INTEGER"}},"required":["path"]},"handler":disk_folder_usage}