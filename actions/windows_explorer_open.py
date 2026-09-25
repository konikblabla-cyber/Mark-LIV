"""Open Windows Explorer at a path."""
import platform,subprocess
from pathlib import Path
def windows_explorer_open(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; path=Path(str(p.get("path") or Path.home())).expanduser()
 if not path.exists():return f"Path not found: {path}"
 subprocess.Popen(["explorer.exe",str(path)],shell=False)
 return f"Opened Explorer: {path}"
TOOL={"name":"windows_explorer_open","description":"Open Windows File Explorer directly at an existing file or folder path.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}}},"handler":windows_explorer_open}
