"""Bounded Windows directory event watcher using PowerShell Register-ObjectEvent."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_file_event_watch(parameters=None,**kwargs):
 p=parameters or {}; root=str(p.get("path","")).strip(); seconds=max(.5,min(float(p.get("seconds",10)),30))
 if not root:return "Directory path is required."
 ps=f"$p=Join-Path $env:TEMP 'markliv_watch_$([guid]::NewGuid().ToString()).log'; $w=New-Object IO.FileSystemWatcher; $w.Path='{root.replace("'","''")}'; $w.IncludeSubdirectories=$true; $w.EnableRaisingEvents=$true; $a={{Add-Content $p ('{0}|' -f $Event.SourceEventArgs.ChangeType + $Event.SourceEventArgs.FullPath)}}; Register-ObjectEvent $w Created -Action $a | Out-Null; Register-ObjectEvent $w Changed -Action $a | Out-Null; Register-ObjectEvent $w Deleted -Action $a | Out-Null; Register-ObjectEvent $w Renamed -Action $a | Out-Null; Start-Sleep -Seconds {seconds}; Get-Content $p -ErrorAction SilentlyContinue; Remove-Item $p -Force -ErrorAction SilentlyContinue; $w.Dispose()"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",ps],capture_output=True,text=True,timeout=seconds+8,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No file events observed.")[:12000]
TOOL={"name":"windows_file_event_watch","description":"Watch a Windows directory for created, changed, deleted and renamed files for a short bounded period.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"seconds":{"type":"NUMBER"}},"required":["path"]},"handler":windows_file_event_watch}
