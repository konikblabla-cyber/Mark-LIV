"""Open a file with a specific Windows application."""
import os, platform, subprocess

def windows_file_open_with(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    p=parameters or {}
    path=os.path.abspath(str(p.get("path","")))
    app=str(p.get("application","")).strip()
    if not path or not os.path.isfile(path): return "File does not exist."
    if not app:return "Missing application."
    try:
        subprocess.Popen([app, path], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
    except OSError as e:
        return f"Application start failed: {e}"
    return f"Opened file with application: {app}"

TOOL={"name":"windows_file_open_with","description":"Open an existing Windows file using a specified application executable.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"application":{"type":"STRING"}},"required":["path","application"]},"handler=windows_file_open_with}
