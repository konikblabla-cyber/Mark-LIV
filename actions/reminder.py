"""Windows-only timed reminders using Task Scheduler."""
import json, platform, subprocess, sys
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

if platform.system() != "Windows":
    raise RuntimeError("Mark-LIV is Windows-only.")

_HIDDEN={"creationflags": subprocess.CREATE_NO_WINDOW}
_MAX_MESSAGE=500

def _scripts_dir():
    path=Path.home()/".jarvis"/"reminders"
    path.mkdir(parents=True,exist_ok=True)
    return path

def _sanitize(text):
    text=" ".join(str(text or "Reminder").replace("\\"," ").replace("\r"," ").replace("\n"," ").split())
    return text[:_MAX_MESSAGE] or "Reminder"

def _write_notify_script(task_name,message):
    path=_scripts_dir()/f"{task_name}.py"
    literal=json.dumps(message,ensure_ascii=False)
    body=f'''import pathlib
message={literal}
notified=False
try:
    from win10toast import ToastNotifier
    ToastNotifier().show_toast("J.A.R.V.I.S Reminder",message,duration=15,threaded=False)
    notified=True
except Exception:
    pass
if not notified:
    try:
        import subprocess
        subprocess.run(["msg","*","/TIME:30",message],check=False,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
    except Exception:
        pass
try:
    import winsound,time
    for freq in (800,1000,1200):
        winsound.Beep(freq,180)
        time.sleep(0.08)
except Exception:
    pass
try:
    pathlib.Path(__file__).unlink(missing_ok=True)
except Exception:
    pass
'''
    path.write_text(body,encoding="utf-8")
    return path

def _schedule_windows(target_dt,task_name,script_path):
    python_exe=Path(sys.executable)
    pythonw=python_exe.parent/"pythonw.exe"
    if pythonw.exists(): python_exe=pythonw
    xml_path=_scripts_dir()/f"{task_name}.xml"
    command=escape(str(python_exe)); args=escape(f'"{script_path}"')
    xml=f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
<RegistrationInfo><Description>J.A.R.V.I.S Reminder</Description></RegistrationInfo>
<Triggers><TimeTrigger><StartBoundary>{target_dt.strftime("%Y-%m-%dT%H:%M:%S")}</StartBoundary><Enabled>true</Enabled></TimeTrigger></Triggers>
<Actions Context="Author"><Exec><Command>{command}</Command><Arguments>{args}</Arguments></Exec></Actions>
<Settings><MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy><DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries><StopIfGoingOnBatteries>false</StopIfGoingOnBatteries><StartWhenAvailable>true</StartWhenAvailable><ExecutionTimeLimit>PT5M</ExecutionTimeLimit><Enabled>true</Enabled></Settings>
<Principals><Principal id="Author"><LogonType>InteractiveToken</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
</Task>'''
    xml_path.write_text(xml,encoding="utf-16")
    try:
        r=subprocess.run(["schtasks.exe","/Create","/TN",task_name,"/XML",str(xml_path),"/F"],capture_output=True,text=True,timeout=30,**_HIDDEN)
    finally:
        xml_path.unlink(missing_ok=True)
    if r.returncode!=0:
        script_path.unlink(missing_ok=True)
        return ""
    return task_name

def reminder(parameters, response=None, player=None, session_memory=None):
    p=parameters or {}
    date_str=str(p.get("date","")).strip()
    time_str=str(p.get("time","")).strip()
    message=_sanitize(p.get("message","Reminder"))
    if not date_str or not time_str:
        return "I need both a date and a time."
    try:
        target=datetime.strptime(f"{date_str} {time_str}","%Y-%m-%d %H:%M")
    except ValueError:
        return "Use date YYYY-MM-DD and time HH:MM."
    now=datetime.now()
    if target<=now: return "That reminder time has already passed."
    task_name=f"JARVISReminder_{target.strftime('%Y%m%d_%H%M%S')}"
    try:
        script=_write_notify_script(task_name,message)
        job=_schedule_windows(target,task_name,script)
    except Exception as exc:
        try: script.unlink(missing_ok=True)
        except Exception: pass
        return f"Could not schedule reminder: {exc}"
    if not job: return "Windows Task Scheduler could not register the reminder."
    if player:
        try: player.write_log(f"[Reminder] {date_str} {time_str} — {message[:60]}")
        except Exception: pass
    return f"Reminder set for {target.strftime('%Y-%m-%d at %H:%M')}."

TOOL={"name":"reminder","description":"Set a one-time Windows Task Scheduler reminder with a desktop notification.","parameters":{"type":"OBJECT","properties":{"date":{"type":"STRING","description":"YYYY-MM-DD"},"time":{"type":"STRING","description":"HH:MM (24-hour)"},"message":{"type":"STRING","description":"Reminder text"}},"required":["date","time","message"]},"handler":reminder}
