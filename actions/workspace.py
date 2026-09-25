"""Named Windows workspaces for Mark-LIV."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
WORKSPACES={"gaming":["steam.exe"],"school":["notepad.exe"],"coding":["code.exe"]}
def workspace(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","list")).lower().strip(); name=str(p.get("name","")).lower().strip()
 if a=="list": return "Available workspaces: "+", ".join(sorted(WORKSPACES))
 if a=="open":
  apps=WORKSPACES.get(name)
  if not apps:return "Unknown workspace. Use list."
  result=[]
  for app in apps:
   try: subprocess.Popen([app],creationflags=subprocess.CREATE_NO_WINDOW); result.append(app)
   except OSError: result.append(f"{app} (not installed)")
  return f"Workspace {name}: "+", ".join(result)
 return "Unknown workspace action."
TOOL={"name":"workspace","description":"Windows-only named workspace launcher: list or open predefined gaming, school, or coding application sets. Missing apps are reported, not installed.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"name":{"type":"STRING"}},"required":["action"]},"handler":workspace}
