"""Search PATH entries for a named executable."""
import os,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_path_search(parameters=None,**kwargs):
 name=str((parameters or {}).get("name") or "").strip()
 if not name:return "Missing executable name."
 if not name.lower().endswith(".exe"):name+=".exe"
 found=[]
 for d in os.environ.get("PATH","").split(os.pathsep):
  if not d:continue
  p=os.path.join(d,name)
  if os.path.isfile(p):found.append(p)
 return "\n".join(found[:100]) if found else f"Not found in PATH: {name}"
TOOL={"name":"windows_path_search","description":"Find an executable by exact filename in the current Windows PATH.","parameters":{"type":"OBJECT","properties":{"name":{"type":"STRING"}},"required":["name"]},"handler=windows_path_search}
