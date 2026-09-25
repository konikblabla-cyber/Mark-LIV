"""Safe, bounded Windows maintenance actions."""
import platform,os,tempfile,shutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_safe_maintenance(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","report")).lower()
 if a=="report":
  paths=[tempfile.gettempdir(),os.environ.get("LOCALAPPDATA","")]
  rows=[]
  for root in paths:
   if root and os.path.isdir(root):
    count=0;size=0
    for base,dirs,files in os.walk(root):
     for f in files:
      try:size+=os.path.getsize(os.path.join(base,f));count+=1
      except OSError:pass
      if count>=5000:break
     if count>=5000:break
    rows.append(f"{root}: {count} files, {size/1024**2:.1f} MB")
  return "\n".join(rows) or "No temp locations available."
 if a=="clear_temp":
  root=tempfile.gettempdir(); removed=0
  for name in os.listdir(root):
   path=os.path.join(root,name)
   try:
    if os.path.isdir(path): shutil.rmtree(path);removed+=1
    else: os.remove(path);removed+=1
   except OSError:pass
  return f"Cleared {removed} accessible TEMP items; files in use were skipped."
 return "Action must be report or clear_temp."
TOOL={"name":"windows_safe_maintenance","description":"Bounded Windows TEMP maintenance: report usage or clear accessible TEMP items. Clear is destructive to temporary files but does not touch user documents.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_safe_maintenance}
