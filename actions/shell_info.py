"""Windows shell/environment information for Mark-LIV."""
import platform,os,subprocess
def shell_info(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; a=str(p.get("action","env")).lower().strip()
 if a=="env":
  keys=["USERNAME","USERPROFILE","COMPUTERNAME","TEMP","APPDATA","LOCALAPPDATA","PROGRAMFILES","WINDIR"]
  return "\n".join(f"{k}={os.environ.get(k,'')}" for k in keys)
 if a=="paths":
  r=subprocess.run(["where.exe","powershell.exe","cmd.exe","explorer.exe"],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW)
  return r.stdout.strip() or r.stderr.strip() or "No shell paths found."
 if a=="version":
  r=subprocess.run(["cmd.exe","/c","ver"],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW)
  return r.stdout.strip() or "Windows version unavailable."
 return "Unknown shell_info action."
TOOL={"name":"shell_info","description":"Windows-only shell/environment diagnostics: safe environment identity fields, core executable paths, and command shell version.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":shell_info}
