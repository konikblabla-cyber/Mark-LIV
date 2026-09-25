"""Bounded Windows executable catalog with publisher and signature status."""
import platform,subprocess
def windows_exe_catalog(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; root=str(p.get("root",r"C:\Program Files")).strip() or r"C:\Program Files"; limit=max(1,min(int(p.get("limit",100)),300))
 safe=root.replace("'","''")
 cmd=f"Get-ChildItem '{safe}' -Filter *.exe -Recurse -ErrorAction SilentlyContinue | Select -First {limit} | ForEach-Object {{$s=Get-AuthenticodeSignature $_.FullName -ErrorAction SilentlyContinue; [PSCustomObject]@{{Name=$_.Name;Path=$_.FullName;Size=$_.Length;Company=$_.VersionInfo.CompanyName;Version=$_.VersionInfo.FileVersion;Signature=$s.Status}}}} | Format-Table -Wrap -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No executables found.")[:24000]
TOOL={"name":"windows_exe_catalog","description":"Read-only bounded catalog of Windows executables with company, version and signature status.","parameters":{"type":"OBJECT","properties":{"root":{"type":"STRING"},"limit":{"type":"INTEGER"}}},"handler":windows_exe_catalog}
