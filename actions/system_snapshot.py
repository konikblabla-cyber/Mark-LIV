"""Windows-only consolidated system snapshot for autonomous decisions."""
import platform, subprocess
def system_snapshot(parameters=None, **kwargs):
    if platform.system()!="Windows": return "Windows-only action."
    commands=[
        ("system","Get-CimInstance Win32_OperatingSystem | Select Caption,Version,LastBootUpTime | Format-List"),
        ("cpu","Get-CimInstance Win32_Processor | Select Name,NumberOfLogicalProcessors,LoadPercentage | Format-List"),
        ("memory","Get-CimInstance Win32_OperatingSystem | Select TotalVisibleMemorySize,FreePhysicalMemory | Format-List"),
        ("gpu","Get-CimInstance Win32_VideoController | Select Name,DriverVersion | Format-List"),
        ("disk","Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | Select DeviceID,Size,FreeSpace | Format-Table -AutoSize")
    ]
    out=[]
    for name,cmd in commands:
        try:
            r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
        except (subprocess.TimeoutExpired,OSError) as e:
            out.append(f"[{name}] failed: {e}")
            continue
        out.append(f"[{name}]\n{(r.stdout or r.stderr).strip()}")
    return "\n\n".join(out)[:16000]
TOOL={"name":"system_snapshot","description":"Windows-only consolidated system snapshot: OS, CPU/load, memory, GPU/driver and local disk capacity in one action, useful before deciding which system actions to perform.","parameters":{"type":"OBJECT","properties":{},"required":[]},"handler":system_snapshot}
