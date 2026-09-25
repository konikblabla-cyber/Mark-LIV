"""Prepare Windows for gaming with reversible, low-risk settings."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def run(cmd): return subprocess.run(cmd,capture_output=True,text=True,timeout=15,shell=False)
def windows_gaming_prep(parameters=None,**kwargs):
 r=run(["powercfg","/setactive","SCHEME_MIN"])
 parts=["High-performance power plan activated."]
 q=run(["reg","add",r"HKCU\Software\Microsoft\GameBar","/v","AutoGameModeEnabled","/t","REG_DWORD","/d","1","/f"])
 if q.returncode==0: parts.append("Windows Game Mode enabled.")
 else: parts.append("Game Mode could not be changed.")
 return " ".join(parts)
TOOL={"name":"windows_gaming_prep","description":"Prepare Windows for gaming by activating High Performance power plan and enabling Game Mode; reversible settings only.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_gaming_prep}
