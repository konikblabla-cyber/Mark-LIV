"""Windows GPU utilization snapshot via performance counters."""
import platform
import subprocess

def windows_gpu_usage(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    cmd = "Get-Counter '\\GPU Engine(*)\\Utilization Percentage' -ErrorAction SilentlyContinue | Select -ExpandProperty CounterSamples | Sort CookedValue -Descending | Select -First 20 InstanceName,CookedValue | Format-Table -AutoSize"
    try:
        r = subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd], capture_output=True, text=True, timeout=15, creationflags=subprocess.CREATE_NO_WINDOW)
        return (r.stdout or r.stderr or "No GPU utilization counters available.")[:10000]
    except (OSError, subprocess.SubprocessError) as exc:
        return f"Could not read GPU utilization: {exc}"

TOOL={"name":"windows_gpu_usage","description":"Read-only Windows GPU engine utilization snapshot.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_gpu_usage}
