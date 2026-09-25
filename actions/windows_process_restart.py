"""Controlled restart of a Windows process by executable name."""
import platform,subprocess,os,time,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
PROTECTED={"system","registry","smss.exe","csrss.exe","wininit.exe","winlogon.exe","services.exe","lsass.exe","svchost.exe","dwm.exe","explorer.exe"}
def windows_process_restart(parameters=None,**kwargs):
 p=parameters or {}; exe=os.path.basename(str(p.get("exe") or "").strip())
 if not exe:return "Executable name required."
 if exe.casefold() in PROTECTED:return "Protected Windows process; restart is blocked."
 matches=[x for x in psutil.process_iter(["name"]) if (x.info.get("name") or "").casefold()==exe.casefold()]
 for x in matches:
  try:x.terminate()
  except (psutil.NoSuchProcess,psutil.AccessDenied):pass
 psutil.wait_procs(matches,timeout=5)
 launch=str(p.get("command") or exe).strip()
 try: subprocess.Popen(launch,creationflags=subprocess.CREATE_NO_WINDOW,shell=False); time.sleep(.5)
 except OSError as e:return f"Could not restart {exe}: {e}"
 return f"Restart requested for {exe}."
TOOL={"name":"windows_process_restart","description":"Controlled restart of a named Windows application process; blocks critical Windows processes. Use only when the user explicitly asks to restart that application.","parameters":{"type":"OBJECT","properties":{"exe":{"type":"STRING"},"command":{"type":"STRING"}},"required":["exe"]},"handler":windows_process_restart}
