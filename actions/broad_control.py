import os
import platform
import subprocess
import shlex
from core import confirm

try:
    from core.permissions import needs_confirmation
except (ImportError, ModuleNotFoundError):
    def needs_confirmation(action: str, *, admin: bool = False) -> bool:
        return False

_OS = platform.system()
_WIN_HIDE = {"creationflags": subprocess.CREATE_NO_WINDOW} if _OS == "Windows" else {}

def _ps(command):
    return subprocess.run(["powershell","-NoProfile","-NonInteractive","-Command",command],
                          capture_output=True,text=True,timeout=15,**_WIN_HIDE)

def _execute(op, value=""):
    if _OS != "Windows":
        return "Windows-only action."
    if op == "launch":
        subprocess.Popen(shlex.split(value, posix=False), shell=False)
        return f"Launched: {value}"
    if op in ("open_file","open_folder"):
        os.startfile(value); return f"Opened: {value}"
    if op == "close_active":
        _ps('(New-Object -ComObject WScript.Shell).SendKeys("%{F4}")')
        return "Requested close of active window."
    if op == "lock":
        subprocess.run(["rundll32.exe","user32.dll,LockWorkStation"],capture_output=True)
        return "PC locked."
    if op == "sleep":
        subprocess.run(["rundll32.exe","powrprof.dll,SetSuspendState","0","1","0"],capture_output=True)
        return "PC sleep requested."
    if op in ("shutdown","restart","logoff"):
        cmd={"shutdown":"shutdown /s /t 0","restart":"shutdown /r /t 0","logoff":"shutdown /l"}[op]
        subprocess.run(cmd,shell=True,capture_output=True,**_WIN_HIDE)
        return f"{op} requested."
    if op == "task_manager":
        subprocess.Popen(["taskmgr.exe"],**_WIN_HIDE); return "Task Manager opened."
    if op == "device_manager":
        subprocess.Popen(["devmgmt.msc"],shell=True,**_WIN_HIDE); return "Device Manager opened."
    if op == "services":
        subprocess.Popen(["services.msc"],shell=True,**_WIN_HIDE); return "Services opened."
    if op == "settings":
        subprocess.Popen(["explorer.exe","ms-settings:"],**_WIN_HIDE); return "Settings opened."
    if op == "control_panel":
        subprocess.Popen(["control.exe"],**_WIN_HIDE); return "Control Panel opened."
    if op == "network_connections":
        subprocess.Popen(["explorer.exe","ncpa.cpl"],**_WIN_HIDE); return "Network Connections opened."
    if op == "process_list":
        r=_ps("Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 30 Id,ProcessName,@{N='RAM_MB';E={[math]::Round($_.WorkingSet64/1MB)}} | Format-Table -AutoSize | Out-String")
        return r.stdout.strip() or "No process data."
    if op == "process_stop":
        try: pid=int(value)
        except ValueError: return "PID required."
        protected={"system","registry","smss","csrss","wininit","winlogon","services","lsass","svchost","dwm","explorer"}
        r=_ps(f"(Get-Process -Id {pid} -ErrorAction SilentlyContinue).ProcessName")
        name=r.stdout.strip().lower()
        if not name: return f"PID {pid} not found."
        if name in protected: return f"Protected process refused: {name}."
        _ps(f"Stop-Process -Id {pid} -Force")
        return f"Stopped {name} (PID {pid})."
    return f"Unknown operation: {op}"

def broad_control(parameters=None, response=None, player=None, session_memory=None):
    p=parameters or {}; op=str(p.get("operation","")).strip().lower(); value=str(p.get("value","")).strip()
    allowed={"launch","open_file","open_folder","close_active","lock","sleep","shutdown","restart","logoff",
             "task_manager","device_manager","services","settings","control_panel","network_connections",
             "process_list","process_stop"}
    if op not in allowed: return "Unsupported operation."
    if op in {"launch","open_file","open_folder","process_stop"} and not value: return "A value is required."
    if needs_confirmation(op):
        if confirm.pending_title(): return "There is already a confirmation waiting on screen."
        return confirm.request(key=f"broad_control:{op}",title="Allow JARVIS to perform this computer action?",
                               detail=f"Operation: {op}\nTarget: {value or '(current computer)'}",
                               run=lambda: _execute(op,value))
    return _execute(op,value)

TOOL={"name":"broad_control",
"description":"Windows-only direct computer control: launch/open/close/lock/sleep, shutdown/restart/logoff, Task Manager, Device Manager, Services, Settings, Control Panel, network connections, process listing and safe process termination.",
"parameters":{"type":"OBJECT","properties":{
"operation":{"type":"STRING","description":"launch | open_file | open_folder | close_active | lock | sleep | shutdown | restart | logoff | task_manager | device_manager | services | settings | control_panel | network_connections | process_list | process_stop"},
"value":{"type":"STRING","description":"Path, program, or PID when required."}},"required":["operation"]},"handler":broad_control}
