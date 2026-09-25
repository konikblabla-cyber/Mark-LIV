"""Windows path accessibility checks."""
import platform,os
from pathlib import Path
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_path_check(parameters=None,**kwargs):
 p=parameters or {}; path=Path(str(p.get("path","")))
 if not path.exists():return "Path does not exist."
 return "\n".join([f"Path: {path}",f"Type: {'directory' if path.is_dir() else 'file'}",f"Readable: {os.access(path,os.R_OK)}",f"Writable: {os.access(path,os.W_OK)}",f"Executable: {os.access(path,os.X_OK)}"])
TOOL={"name":"windows_path_check","description":"Read-only Windows path existence, type and local access check.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}},"required":["path"]},"handler":windows_path_check}
