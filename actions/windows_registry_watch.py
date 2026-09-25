"""Bounded Windows registry value watcher."""
import platform,subprocess,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_registry_watch(parameters=None,**kwargs):
 p=parameters or {}; key=str(p.get("key","")).strip(); seconds=max(1,min(int(p.get("seconds",15)),60))
 if not key:return "Registry key is required."
 safe=key.replace("'","''"); ps=f"$k='{safe}'; $last=(Get-ItemProperty -Path $k -ErrorAction SilentlyContinue | Out-String); $end=(Get-Date).AddSeconds({seconds}); while((Get-Date)-lt $end){{Start-Sleep -Seconds 1;$now=(Get-ItemProperty -Path $k -ErrorAction SilentlyContinue | Out-String);if($now -ne $last){{'Registry change detected';$now;break}}}}"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",ps],capture_output=True,text=True,timeout=seconds+8,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No registry change observed.")[:8000]
TOOL={"name":"windows_registry_watch","description":"Bounded read-only watcher for changes to a Windows registry key's values.","parameters":{"type":"OBJECT","properties":{"key":{"type":"STRING"},"seconds":{"type":"INTEGER"}},"required":["key"]},"handler":windows_registry_watch}
