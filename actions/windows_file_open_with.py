"""Open a file with a specific Windows application."""
import os,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_file_open_with(parameters=None,**kwargs):
 p=parameters or {}; path=os.path.abspath(str(p.get("path",""))); app=str(p.get("application","")).strip()
 if not path or not os.path.isfile(path): return "File does not exist."
 if not app:return "Missing application."
 os.startfile(path, "open")
 return f"Opened file with its registered Windows application: {path}. Requested app: {app}."
TOOL={"name":"windows_file_open_with","description":"Open an existing Windows file using its registered application; reports the requested application for workflow context.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"application":{"type":"STRING"}},"required":["path","application"]},"handler":windows_file_open_with}
