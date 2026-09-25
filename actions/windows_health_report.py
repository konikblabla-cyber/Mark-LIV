"""Compact Windows health report for Mark-LIV."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_health_report(parameters=None,**kwargs):
 cmd="Get-CimInstance Win32_OperatingSystem | Select Caption,Version,LastBootUpTime,FreePhysicalMemory,TotalVisibleMemorySize | Format-List; Get-CimInstance Win32_Processor | Select Name,LoadPercentage | Format-Table -AutoSize; Get-Volume | Where-Object DriveLetter | Select DriveLetter,SizeRemaining,Size,HealthStatus | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No health report.")[:12000]
TOOL={"name":"windows_health_report","description":"Read-only compact Windows health report covering OS boot, RAM, CPU load and drive capacity/health.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_health_report}
