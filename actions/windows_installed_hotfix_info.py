"""Read-only detailed Windows hotfix inspection."""
import platform,subprocess

def windows_installed_hotfix_info(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; q=str(p.get("query","")).strip(); safe=q.replace("'","''")
 cmd="Get-HotFix | Sort-Object InstalledOn -Descending"
 if safe:cmd+=f" | Where-Object {{$_.HotFixID -like '*{safe}*' -or $_.Description -like '*{safe}*'}}"
 cmd+=" | Select HotFixID,Description,InstalledOn,InstalledBy,PSComputerName | Format-Table -AutoSize"
 try:r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 except (OSError,subprocess.SubprocessError) as e:return f"Hotfix inspection failed: {e}"
 return (r.stdout or r.stderr or "No matching hotfixes found.")[:14000]
TOOL={"name":"windows_installed_hotfix_info","description":"Read-only detailed Windows hotfix and update inspection, optionally filtered.","parameters":{"type":"OBJECT","properties":{"query":{"type":"STRING"}}},"handler":windows_installed_hotfix_info}