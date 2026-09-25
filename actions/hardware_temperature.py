"""Windows hardware temperature sensors via WMI when available."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def hardware_temperature(parameters=None,**kwargs):
 cmd="Get-CimInstance MSAcpi_ThermalZoneTemperature -Namespace root/wmi -ErrorAction SilentlyContinue | Select InstanceName,CurrentTemperature | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 if not r.stdout.strip():return "Windows exposed no thermal-zone temperature sensors."
 return r.stdout[:8000]
TOOL={"name":"hardware_temperature","description":"Read-only Windows thermal-zone temperature sensor query when firmware exposes sensors through WMI; missing sensors are reported honestly.","parameters":{"type":"OBJECT","properties":{}},"handler":hardware_temperature}
