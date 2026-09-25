"""Windows storage inspection helpers for Mark-LIV."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def storage_tools(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","volumes")).lower().strip()
 cmds={"volumes":"Get-Volume | Select DriveLetter,FileSystemLabel,FileSystem,Size,SizeRemaining,HealthStatus | Format-Table -AutoSize","disks":"Get-Disk | Select Number,FriendlyName,BusType,HealthStatus,OperationalStatus,Size | Format-Table -AutoSize","partitions":"Get-Partition | Select DiskNumber,PartitionNumber,DriveLetter,Size,Type | Format-Table -AutoSize"}
 if a not in cmds:return "Use volumes, disks or partitions."
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmds[a]],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No storage data.")[:10000]
TOOL={"name":"storage_tools","description":"Windows-only storage inventory: volumes, physical disks and partitions with capacity and health information. Read-only.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":storage_tools}
