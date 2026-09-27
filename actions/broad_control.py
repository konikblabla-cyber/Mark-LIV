"""Windows-only broad computer controls with explicit safety checks."""
import os
import platform
import shlex
import subprocess
from core import confirm

try:
    from core.permissions import command_needs_admin, is_admin, is_admin_failure, needs_confirmation
except (ImportError, ModuleNotFoundError):
    def needs_confirmation(action: str, *, admin: bool = False) -> bool:
        return False

_HIDDEN={"creationflags":subprocess.CREATE_NO_WINDOW}
_OS = platform.system()
_PROTECTED={"system","registry","smss","csrss","wininit","winlogon","services","lsass","svchost","dwm","explorer"}
_ALLOWED={"launch","open_file","open_folder","close_active","lock","sleep","shutdown","restart","logoff","task_manager","device_manager","services","settings","control_panel","network_connections","process_list","process_stop","run_command","run_as_admin"}

def _ps(command: str, timeout: int = 15):
    return subprocess.run(["powershell","-NoProfile","-NonInteractive","-Command",command],capture_output=True,text=True,timeout=max(1,min(timeout,60)),**_HIDDEN)

def _execute(op: str, value: str = "") -> str:
    try:
        if op=="launch":
            args=shlex.split(value,posix=False)
            if not args:return "Program is required."
            subprocess.Popen(args,shell=False,**_HIDDEN);return f"Launched: {value}"
        if op in {"open_file","open_folder"}:
            path=os.path.abspath(os.path.expandvars(os.path.expanduser(value)))
            if not os.path.exists(path):return f"Path not found: {path}"
            os.startfile(path);return f"Opened: {path}"
        if op=="close_active":
            r=_ps('(New-Object -ComObject WScript.Shell).SendKeys("%{F4}")')
            return "Requested close of active window." if r.returncode==0 else "Could not request window close."
        if op=="lock":
            r=subprocess.run(["rundll32.exe","user32.dll,LockWorkStation"],capture_output=True,**_HIDDEN)
            return "PC locked." if r.returncode==0 else "Could not lock the PC."
        if op=="sleep":
            r=subprocess.run(["rundll32.exe","powrprof.dll,SetSuspendState","0","1","0"],capture_output=True,**_HIDDEN)
            return "PC sleep requested." if r.returncode==0 else "Could not request sleep."
        if op in {"shutdown","restart","logoff"}:
            cmd={"shutdown":["shutdown.exe","/s","/t","0"],"restart":["shutdown.exe","/r","/t","0"],"logoff":["shutdown.exe","/l"]}[op]
            r=subprocess.run(cmd,capture_output=True,**_HIDDEN)
            err=r.stderr.decode(errors="replace").strip() if isinstance(r.stderr,bytes) else str(r.stderr).strip()
            return f"{op} requested." if r.returncode==0 else (err or f"{op} failed.")
        if op=="task_manager":subprocess.Popen(["taskmgr.exe"],**_HIDDEN);return "Task Manager opened."
        if op=="device_manager":subprocess.Popen(["mmc.exe","devmgmt.msc"],**_HIDDEN);return "Device Manager opened."
        if op=="services":subprocess.Popen(["mmc.exe","services.msc"],**_HIDDEN);return "Services opened."
        if op=="settings":subprocess.Popen(["explorer.exe","ms-settings:"],**_HIDDEN);return "Settings opened."
        if op=="control_panel":subprocess.Popen(["control.exe"],**_HIDDEN);return "Control Panel opened."
        if op=="network_connections":subprocess.Popen(["explorer.exe","ncpa.cpl"],**_HIDDEN);return "Network Connections opened."
        if op=="process_list":
            r=_ps("Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 30 Id,ProcessName,@{N='RAM_MB';E={[math]::Round($_.WorkingSet64/1MB)}} | ConvertTo-Csv -NoTypeInformation")
            return r.stdout.strip() or "No process data."
        if op=="run_command":
            if not value:return "A command is required."
            try:
                r=subprocess.run(value, shell=True, capture_output=True, text=True, timeout=60, **_HIDDEN)
                output=(r.stdout or r.stderr or "").strip()
                return f"Command exit={r.returncode}:\n{output[:8000]}" if output else f"Command exit={r.returncode}."
            except subprocess.TimeoutExpired:
                return "Command timed out after 60 seconds."
        if op=="run_as_admin":
            if not value:return "A command is required."
            escaped=value.replace('"','\\\"')
            r=subprocess.run(["powershell","-NoProfile","-NonInteractive","-Command",f"Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -Command \\\"{escaped}\\\"'"],capture_output=True,text=True,timeout=15,**_HIDDEN)
            return "Administrator command requested." if r.returncode==0 else (r.stderr.strip() or "Administrator command failed.")
        if op=="process_stop":
            try:pid=int(value)
            except (TypeError,ValueError):return "PID required."
            if pid<=4:return f"Refused to stop protected PID {pid}."
            r=_ps(f"(Get-Process -Id {pid} -ErrorAction SilentlyContinue).ProcessName")
            name=r.stdout.strip().splitlines()[-1].strip().lower() if r.stdout.strip() else ""
            if not name:return f"PID {pid} not found."
            if name in _PROTECTED:return f"Protected process refused: {name}."
            r=_ps(f"Stop-Process -Id {pid} -Force")
            return f"Stopped {name} (PID {pid})." if r.returncode==0 else (r.stderr.strip() or f"Failed to stop PID {pid}.")
    except (OSError,subprocess.SubprocessError,ValueError) as exc:return f"{op} failed: {exc}"
    return f"Unknown operation: {op}"

def broad_control(parameters=None,response=None,player=None,session_memory=None):
    if platform.system()!="Windows":return "Windows-only action."
    p=parameters or {};op=str(p.get("operation","")).strip().lower();value=str(p.get("target", p.get("value",""))).strip()
    if op not in _ALLOWED:return "Unsupported operation."
    if op in {"launch","open_file","open_folder","process_stop","run_command","run_as_admin"} and not value:return "A target is required."
    admin_hint = op=="run_as_admin" or (op=="run_command" and command_needs_admin(value) and not is_admin())
    if admin_hint:
        if confirm.pending_title():return "There is already a confirmation waiting on screen."
        return confirm.request(key=f"broad_control:admin:{op}",title="Allow JARVIS to request administrator access?",detail=f"Command: {value}",run=lambda:_execute("run_as_admin",value)) if needs_confirmation(op,admin=True) else _execute("run_as_admin",value)
    if needs_confirmation(op):
        if confirm.pending_title():return "There is already a confirmation waiting on screen."
        return confirm.request(key=f"broad_control:{op}",title="Allow JARVIS to perform this computer action?",detail=f"Operation: {op}\nTarget: {value or '(current computer)'}",run=lambda:_execute(op,value))
    result = _execute(op,value)
    if op=="run_command" and not is_admin() and is_admin_failure(result):
        if confirm.pending_title():return "Command failed because administrator access is required, but another confirmation is pending."
        return confirm.request(key="broad_control:admin_retry",title="Allow JARVIS to retry the command as administrator?",detail=f"Command: {value}\\nReason: Windows reported that elevation is required.",run=lambda:_execute("run_as_admin",value)) if needs_confirmation(op,admin=True) else _execute("run_as_admin",value)
    return result

TOOL={"name":"broad_control","description":"Windows-only direct computer control for applications, files, windows, power, processes, shell commands and administrator commands. Destructive/shell operations use the central permission gate; Full PC Control can disable confirmations.","parameters":{"type":"OBJECT","properties":{"operation":{"type":"STRING"},"value":{"type":"STRING"}},"required":["operation"]},"handler":broad_control}
