"""Read-only Windows terminal/session information."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_session_info(parameters=None,**kwargs):
 cmd="quser"
 r=subprocess.run([cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW,shell=False)
 return (r.stdout or r.stderr or "No session information available.")[:8000]
TOOL={"name":"windows_session_info","description":"Read-only Windows interactive session information from quser.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_session_info}
