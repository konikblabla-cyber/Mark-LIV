"""Windows GPU inventory."""
import platform
import subprocess

def windows_gpu_info(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    cmd = "Get-CimInstance Win32_VideoController | Select Name,DriverVersion,AdapterRAM,VideoModeDescription,Status | Format-List"
    try:
        r = subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd], capture_output=True, text=True, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
        return (r.stdout or r.stderr or "No GPU information.")[:10000]
    except (OSError, subprocess.SubprocessError) as exc:
        return f"Could not read GPU information: {exc}"

TOOL={"name":"windows_gpu_info","description":"Read-only Windows GPU model, driver, memory and display-mode information.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_gpu_info}
