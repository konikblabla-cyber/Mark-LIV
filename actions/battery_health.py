"""Windows battery health and charge report."""
import platform,subprocess
def battery_health(parameters=None,**kwargs):
 cmd="Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue | Select Name,BatteryStatus,EstimatedChargeRemaining,EstimatedRunTime,DesignVoltage,Status | Format-List"
 if platform.system()!="Windows": return "battery_health is available only on Windows."
 try:
  r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
  return (r.stdout or r.stderr or "No battery detected.")[:8000]
 except (subprocess.TimeoutExpired,OSError) as e:
  return f"Battery health check failed: {e}"
TOOL={"name":"battery_health","description":"Read-only Windows battery status, charge percentage, runtime estimate and voltage when available.","parameters":{"type":"OBJECT","properties":{}},"handler":battery_health}
