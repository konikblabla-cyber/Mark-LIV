"""Bounded batch rename in one Windows directory."""
import os,platform
from core.permissions import permission_decision
from core import confirm
def windows_batch_rename(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {};root=str(p.get("directory","")).strip();prefix=str(p.get("prefix","")).strip()
 if not root or not prefix:return "Missing directory or prefix."
 if not os.path.isdir(root):return f"Directory not found: {root}"
 files=[x for x in os.listdir(root) if os.path.isfile(os.path.join(root,x))][:100]
 plan=[(x,f"{prefix}_{i+1}{os.path.splitext(x)[1]}") for i,x in enumerate(files)]
 if p.get("apply") is not True:return "Preview: "+", ".join(f"{a}->{b}" for a,b in plan[:20])
 if not kwargs.get("_permission_token"):
  decision,reason=permission_decision("windows_batch_rename",p)
  if decision=="deny":return f"Permission denied: {reason}"
  if decision=="confirm":return confirm.request(key="windows_batch_rename",title="Allow JARVIS: windows_batch_rename?",detail=f"{reason}. Waiting for your confirmation.",run=lambda:windows_batch_rename(p,_permission_token=True))
 for a,b in plan:os.rename(os.path.join(root,a),os.path.join(root,b))
 return f"Renamed {len(plan)} files."
TOOL={"name":"windows_batch_rename","description":"Preview or apply a bounded batch rename in one Windows directory.","parameters":{"type":"OBJECT","properties":{"directory":{"type":"STRING"},"prefix":{"type":"STRING"},"apply":{"type":"BOOLEAN"}},"required":["directory","prefix"]},"handler":windows_batch_rename}
