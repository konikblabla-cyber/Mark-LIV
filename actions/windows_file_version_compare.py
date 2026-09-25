"""Read-only Windows file version comparison."""
import platform,subprocess,os
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_file_version_compare(parameters=None,**kwargs):
    if platform.system() != "Windows":
        return "windows_file_version_compare is Windows-only."
 p=parameters or {}; a=str(p.get("file_a","")).strip(); b=str(p.get("file_b","")).strip()
 if not a or not b or not os.path.isfile(a) or not os.path.isfile(b):return "Both file paths must exist."
 def esc(x):return x.replace("'","''")
 cmd=f"$a=Get-Item '{esc(a)}';$b=Get-Item '{esc(b)}'; [PSCustomObject]@{{A=$a.VersionInfo.FileVersion;B=$b.VersionInfo.FileVersion;APath=$a.FullName;BPath=$b.FullName}} | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Version comparison failed.")[:7000]
TOOL={"name":"windows_file_version_compare","description":"Read-only comparison of Windows file version metadata for two existing files.","parameters":{"type":"OBJECT","properties":{"file_a":{"type":"STRING"},"file_b":{"type":"STRING"}},"required":["file_a","file_b"]},"handler":windows_file_version_compare}
