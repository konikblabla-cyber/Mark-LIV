"""Open a Windows terminal in a directory."""
import platform,subprocess
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_terminal_open(parameters=None,**kwargs):
 p=parameters or {}; directory=Path(str(p.get("directory") or Path.home())).expanduser()
 if not directory.is_dir():return f"Directory not found: {directory}"
 subprocess.Popen(["wt.exe","-d",str(directory)],shell=False)
 return f"Opened Windows Terminal in {directory}."
TOOL={"name":"windows_terminal_open","description":"Open Windows Terminal in an existing directory.","parameters":{"type":"OBJECT","properties":{"directory":{"type":"STRING"}}},"handler":windows_terminal_open}
