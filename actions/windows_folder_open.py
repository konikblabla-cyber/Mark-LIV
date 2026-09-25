"""Open an existing Windows folder."""
import os,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_folder_open(parameters=None,**kwargs):
 path=str((parameters or {}).get("path","")).strip()
 if not path or not os.path.isdir(path):return f"Folder not found: {path}"
 os.startfile(path);return f"Opened folder: {path}"
TOOL={"name":"windows_folder_open","description":"Open an existing Windows folder directly in File Explorer.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}},"required":["path"]},"handler=windows_folder_open}
