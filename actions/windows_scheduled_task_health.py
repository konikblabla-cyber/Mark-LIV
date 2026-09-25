"""Read-only Windows scheduled-task health report."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_scheduled_task_health(parameters=None,**kwargs):
 cmd="Get-ScheduledTask | Where-Object {$_.State -eq 'Ready' -or $_.State -eq 'Running'} | ForEach-Object {$i=Get-ScheduledTaskInfo $_.TaskName -TaskPath $_.TaskPath; [PSCustomObject]@{Task=$_.TaskPath+$_.TaskName;State=$_.State;LastRun=$i.LastRunTime;Result=$i.LastTaskResult}} | Sort Task | Format-Table -Wrap -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No scheduled tasks.")[:18000]
TOOL={"name":"windows_scheduled_task_health","description":"Read-only health overview of Windows scheduled tasks, last run times and result codes.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_scheduled_task_health}
