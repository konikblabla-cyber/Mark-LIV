"""Windows GPU utilization snapshot via performance counters."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_gpu_usage(parameters=None,**kwargs):
 cmd="Get-Counter '\\GPU Engine(*)\\Utilization Percentage' -ErrorAction SilentlyContinue | Select -ExpandProperty CounterSamples | Sort CookedValue -Descending | Select -First 20 InstanceName,CookedValue | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No GPU utilization counters available.")[:10000]
TOOL={"name":"windows_gpu_usage","description":"Read-only Windows GPU engine utilization snapshot.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_gpu_usage}
