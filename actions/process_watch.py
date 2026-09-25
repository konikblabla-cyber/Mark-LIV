"""Bounded Windows process monitoring for Mark-LIV."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
_WATCH=set()
def _exists(name):
 r=subprocess.run(["tasklist","/FI",f"IMAGENAME eq {name}"],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=10)
 return name.lower() in r.stdout.lower()
def process_watch(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","status")).lower().strip(); name=str(p.get("process","")).strip()
 if a=="status": return "\n".join(f"{k}: {'running' if _exists(k) else 'not running'}" for k in _WATCH) or "No watched processes."
 if a=="add":
  if not name or len(name)>128 or any(c in name for c in "\\/:*?\"<>|"): return "Valid process executable name required."
  _WATCH.add(name); return f"Watching {name}."
 if a=="remove": _WATCH.discard(name); return f"Stopped watching {name}."
 if a=="check": return f"{name}: {'running' if _exists(name) else 'not running'}" if name else "Process executable name required."
 return "Unknown process_watch action."
TOOL={"name":"process_watch","description":"Windows-only process watcher: add/remove watched executables and check whether they are running. Monitoring is in-memory and never kills processes.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"process":{"type":"STRING"}},"required":["action"]},"handler":process_watch}
