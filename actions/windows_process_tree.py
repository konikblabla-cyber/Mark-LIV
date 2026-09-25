"""Read-only Windows process tree."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_tree(parameters=None,**kwargs):
 cmd="Get-CimInstance Win32_Process | Select ProcessId,ParentProcessId,Name,CommandLine | Sort ParentProcessId,ProcessId | Format-Table -Wrap -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No process tree.")[:20000]
TOOL={"name":"windows_process_tree","description":"Read-only Windows process tree including parent PIDs and command lines.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_process_tree}
