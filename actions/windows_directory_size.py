"""Calculate bounded Windows directory size."""
import os,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_directory_size(parameters=None,**kwargs):
 root=str((parameters or {}).get("directory","")).strip()
 if not root or not os.path.isdir(root):return "Directory not found."
 total=count=0
 for base,dirs,files in os.walk(root):
  for n in files:
   try:total+=os.path.getsize(os.path.join(base,n));count+=1
   except OSError:pass
   if count>=5000:return f"Partial size: {total/1024**3:.2f} GB across {count} files."
 return f"Directory size: {total/1024**3:.2f} GB across {count} files."
TOOL={"name":"windows_directory_size","description":"Calculate bounded total size of a Windows directory.","parameters":{"type":"OBJECT","properties":{"directory":{"type":"STRING"}},"required":["directory"]},"handler":windows_directory_size}
