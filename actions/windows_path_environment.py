"""Read-only Windows executable resolution helper."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_path_environment(parameters=None,**kwargs):
 p=parameters or {}; name=str(p.get("name","")).strip()
 if not name:return "Executable name is required."
 r=subprocess.run(["where.exe",name],capture_output=True,text=True,timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Executable not found on PATH.")[:5000]
TOOL={"name":"windows_path_environment","description":"Read-only resolution of an executable through the Windows PATH.","parameters":{"type":"OBJECT","properties":{"name":{"type":"STRING"}},"required":["name"]},"handler":windows_path_environment}
