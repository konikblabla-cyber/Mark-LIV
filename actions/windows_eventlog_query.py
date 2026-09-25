"""Read-only filtered Windows event log query."""
import platform,subprocess
def windows_eventlog_query(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; log=str(p.get("log","Application")).strip() or "Application"; source=str(p.get("source","")).strip(); n=max(1,min(int(p.get("count",20)),100))
 safe_log=log.replace("'","''"); filt=f"$f=@{{LogName='{safe_log}'"; 
 if source:filt+=f";ProviderName='{source.replace(chr(39),chr(39)+chr(39))}'"
 filt+="}}"
 cmd=f"Get-WinEvent -FilterHashtable {filt} -MaxEvents {n} -ErrorAction SilentlyContinue | Select TimeCreated,Id,LevelDisplayName,ProviderName,Message | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=25,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No matching events found.")[:22000]
TOOL={"name":"windows_eventlog_query","description":"Read-only filtered Windows Event Log query by log/source with bounded results.","parameters":{"type":"OBJECT","properties":{"log":{"type":"STRING"},"source":{"type":"STRING"},"count":{"type":"INTEGER"}}},"handler":windows_eventlog_query}
