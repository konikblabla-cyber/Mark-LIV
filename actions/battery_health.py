"""Windows battery health and charge report."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def battery_health(parameters=None,**kwargs):
 cmd="Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue | Select Name,BatteryStatus,EstimatedChargeRemaining,EstimatedRunTime,DesignVoltage,Status | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No battery detected.")[:8000]
TOOL={"name":"battery_health","description":"Read-only Windows battery status, charge percentage, runtime estimate and voltage when available.","parameters":{"type":"OBJECT","properties":{}},"handler=battery_health}
