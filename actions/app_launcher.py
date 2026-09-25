"""Windows app discovery and launching for Mark-LIV."""
import platform,os,subprocess
from pathlib import Path
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def app_launcher(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","list")).lower().strip(); q=str(p.get("name","")).strip()
 if a=="list":
  roots=[Path(os.environ.get("ProgramFiles",r"C:\Program Files")),Path(os.environ.get("ProgramFiles(x86)",r"C:\Program Files (x86)")),Path(os.environ.get("LOCALAPPDATA",str(Path.home())))/"Programs"]
  out=[]
  for root in roots:
   if root.exists():
    for x in root.rglob("*.exe"):
     if "uninstall" not in x.name.lower(): out.append(str(x))
     if len(out)>=500:break
   if len(out)>=500:break
  return "\n".join(out) or "No applications found."
 if a=="launch":
  if not q:return "Application name or path required."
  if len(q)>260:return "Application name too long."
  try: subprocess.Popen([q],creationflags=subprocess.CREATE_NO_WINDOW); return f"Launched: {q}"
  except OSError:
   matches=[]
   for root in [Path(os.environ.get("ProgramFiles",r"C:\Program Files")),Path(os.environ.get("ProgramFiles(x86)",r"C:\Program Files (x86"))]:
    if root.exists():
     for x in root.rglob("*.exe"):
      if q.casefold() in x.stem.casefold():matches.append(x)
      if len(matches)>=10:break
   if len(matches)==1: os.startfile(str(matches[0])); return f"Launched: {matches[0]}"
   if matches:return "Multiple matches:\n" + "\n".join(map(str,matches))
   return f"Application not found: {q}"
 return "Unknown app_launcher action."
TOOL={"name":"app_launcher","description":"Windows-only application discovery and launching by executable name/path, with safe ambiguity reporting.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"name":{"type":"STRING"}},"required":["action"]},"handler":app_launcher}
