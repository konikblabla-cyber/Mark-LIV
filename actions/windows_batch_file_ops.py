"""Bounded batch file operations on Windows."""
import platform,os,shutil
from core.permissions import permission_decision
from core import confirm
def windows_batch_file_ops(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; op=str(p.get("operation","")).lower(); items=p.get("items") or []
 if op not in ("copy","move","delete") or not isinstance(items,list) or not items:return "Use copy, move or delete with items."
 if len(items)>50:return "Batch limited to 50 items."
 if not kwargs.get("_permission_token"):
  decision,reason=permission_decision("windows_batch_file_ops",p)
  if decision=="deny":return f"Permission denied: {reason}"
  if decision=="confirm":return confirm.request(key="windows_batch_file_ops",title="Allow JARVIS: windows_batch_file_ops?",detail=f"{reason}. Waiting for your confirmation.",run=lambda:windows_batch_file_ops(p,_permission_token=True))
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
