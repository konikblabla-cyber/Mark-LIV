"""Reveal a Windows file or folder in File Explorer."""
import os,platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_path_reveal(parameters=None,**kwargs):
 p=parameters or {}; path=os.path.abspath(str(p.get("path","")))
 if not os.path.exists(path): return "Path does not exist."
 target=path if os.path.isdir(path) else os.path.dirname(path)
 subprocess.Popen(["explorer.exe",f"/select,{path}"] if os.path.isfile(path) else ["explorer.exe",target])
 return f"Revealed in File Explorer: {path}"
TOOL={"name":"windows_path_reveal","description":"Reveal an existing Windows file or folder in File Explorer and select files when possible.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}},"required":["path"]},"handler=windows_path_reveal}
