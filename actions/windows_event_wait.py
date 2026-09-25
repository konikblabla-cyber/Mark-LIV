"""Bounded wait for a matching Windows Application event."""
import platform,subprocess
def windows_event_wait(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; pattern=str(p.get("pattern","")).strip(); seconds=max(1,min(int(p.get("seconds",20)),60))
 if not pattern:return "Event pattern is required."
 ps=f"$end=(Get-Date).AddSeconds({seconds}); do {{$e=Get-WinEvent -FilterHashtable @{{LogName='Application';StartTime=(Get-Date).AddSeconds(-2)}} -MaxEvents 20 -ErrorAction SilentlyContinue | Where-Object {{$_.ProviderName -like '*{pattern.replace("'","''")}*' -or $_.Message -like '*{pattern.replace("'","''")}*'}} | Select-Object -First 1 TimeCreated,Id,ProviderName,Message; if($e){{$e|Format-List;break}}; Start-Sleep -Seconds 1}} while((Get-Date) -lt $end)"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",ps],capture_output=True,text=True,timeout=seconds+8,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No matching event observed.")[:12000]
TOOL={"name":"windows_event_wait","description":"Wait for a matching Windows Application event for a short bounded period.","parameters":{"type":"OBJECT","properties":{"pattern":{"type":"STRING"},"seconds":{"type":"INTEGER"}},"required":["pattern"]},"handler":windows_event_wait}
