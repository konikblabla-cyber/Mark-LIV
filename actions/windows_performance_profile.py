"""Apply a small set of reversible Windows performance profiles."""
import platform,subprocess,winreg
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def _run(args):
 r=subprocess.run(args,capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW);return r.stdout or r.stderr
def windows_performance_profile(parameters=None,**kwargs):
 p=parameters or {}; mode=str(p.get("mode","balanced")).lower()
 if mode not in ("gaming","balanced"):return "Mode must be gaming or balanced."
 if mode=="gaming":
  out=_run(["powercfg.exe","/setactive","SCHEME_MIN"])
  with winreg.CreateKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\GameBar") as k: winreg.SetValueEx(k,"AllowAutoGameMode",0,winreg.REG_DWORD,1)
  return "Gaming profile applied: High Performance power plan and Windows Game Mode enabled."
 out=_run(["powercfg.exe","/setactive","SCHEME_BALANCED"])
 with winreg.CreateKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\GameBar") as k: winreg.SetValueEx(k,"AllowAutoGameMode",0,winreg.REG_DWORD,1)
 return "Balanced profile applied."
TOOL={"name":"windows_performance_profile","description":"Apply reversible Windows performance profiles: gaming (High Performance + Game Mode) or balanced.","parameters":{"type":"OBJECT","properties":{"mode":{"type":"STRING"}},"required":["mode"]},"handler":windows_performance_profile}
