"""Read-only Windows file security metadata."""
import platform,subprocess,os
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_file_security(parameters=None,**kwargs):
 p=parameters or {}; path=str(p.get("path","")).strip()
 if not path or not os.path.exists(path):return "Path is required and must exist."
 safe=path.replace("'","''"); cmd=f"Get-Acl -LiteralPath '{safe}' | Select Owner,AccessToString,AreAccessRulesProtected | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "ACL inspection failed.")[:12000]
TOOL={"name":"windows_file_security","description":"Read-only Windows file owner and ACL inspection.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}},"required":["path"]},"handler":windows_file_security}
