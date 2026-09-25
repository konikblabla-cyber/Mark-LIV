"""Bounded batch file operations on Windows."""
import platform,os,shutil
def windows_batch_file_ops(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; op=str(p.get("operation","")).lower(); items=p.get("items") or []
 if op not in ("copy","move","delete") or not isinstance(items,list) or not items:return "Use copy, move or delete with items."
 if len(items)>50:return "Batch limited to 50 items."
 out=[]
 for x in items:
  if not isinstance(x,dict): continue
  src=os.path.abspath(str(x.get("source") or x.get("path") or ""))
  dst=os.path.abspath(str(x.get("destination") or "")) if x.get("destination") else ""
  if not os.path.isfile(src): out.append(f"missing: {src}"); continue
  if op=="copy":
   if not dst:return "copy requires destination."
   shutil.copy2(src,dst);out.append(f"copied: {src} -> {dst}")
  elif op=="move":
   if not dst:return "move requires destination."
   shutil.move(src,dst);out.append(f"moved: {src} -> {dst}")
  else:
   os.remove(src);out.append(f"deleted: {src}")
 return "\n".join(out)
TOOL={"name":"windows_batch_file_ops","description":"Perform up to 50 explicit Windows file copy, move, or delete operations in one call.","parameters":{"type":"OBJECT","properties":{"operation":{"type":"STRING"},"items":{"type":"ARRAY"}},"required":["operation","items"]},"handler":windows_batch_file_ops}
