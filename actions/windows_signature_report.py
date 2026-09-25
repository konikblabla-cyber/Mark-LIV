"""Read-only Authenticode signature report for executable files."""
import platform,subprocess,os
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_signature_report(parameters=None,**kwargs):
 p=parameters or {}; path=str(p.get("path","")).strip()
 if not path or not os.path.isfile(path):return "File path is required."
 safe=path.replace("'","''"); cmd=f"Get-AuthenticodeSignature '{safe}' | Select Status,StatusMessage,Path,@{{N='Signer';E={{$_.SignerCertificate.Subject}}}} | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Signature check failed.")[:6000]
TOOL={"name":"windows_signature_report","description":"Read-only Authenticode signature verification report for a Windows file.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}},"required":["path"]},"handler":windows_signature_report}
