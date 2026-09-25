"""Read-only Windows executable metadata analysis."""
import platform,subprocess,os
def windows_exe_analysis(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; path=str(p.get("path","")).strip()
 if not path or not os.path.isfile(path):return "Executable file path is required."
 safe=path.replace("'","''")
 cmd=f"$i=Get-Item '{safe}' -ErrorAction Stop; $s=Get-AuthenticodeSignature '{safe}' -ErrorAction SilentlyContinue; [PSCustomObject]@{{Name=$i.Name;Path=$i.FullName;Size=$i.Length;Created=$i.CreationTime;Modified=$i.LastWriteTime;Version=$i.VersionInfo.FileVersion;Company=$i.VersionInfo.CompanyName;Product=$i.VersionInfo.ProductName;Signature=$s.Status;Signer=$s.SignerCertificate.Subject}} | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Analysis failed.")[:10000]
TOOL={"name":"windows_exe_analysis","description":"Read-only Windows executable metadata, publisher and Authenticode signature analysis.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}},"required":["path"]},"handler":windows_exe_analysis}
