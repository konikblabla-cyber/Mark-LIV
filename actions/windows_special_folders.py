"""Open common Windows user folders."""
import os,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
FOLDERS={"desktop":"Desktop","documents":"Documents","downloads":"Downloads","pictures":"Pictures","videos":"Videos","music":"Music"}
def windows_special_folders(parameters=None,**kwargs):
 p=parameters or {}; name=str(p.get("folder","")).lower()
 if name not in FOLDERS:return "Folder must be desktop, documents, downloads, pictures, videos, or music."
 path=os.path.join(os.environ.get("USERPROFILE",""),FOLDERS[name])
 os.startfile(path);return f"Opened {name}: {path}"
TOOL={"name":"windows_special_folders","description":"Open a common Windows user folder such as Downloads or Documents.","parameters":{"type":"OBJECT","properties":{"folder":{"type":"STRING"}},"required":["folder"]},"handler":windows_special_folders}
