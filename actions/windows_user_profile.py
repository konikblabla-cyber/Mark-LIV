"""Windows user-profile inspection."""
import platform,os
from pathlib import Path
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_user_profile(parameters=None,**kwargs):
 home=Path(os.environ.get("USERPROFILE",str(Path.home())))
 keys=["APPDATA","LOCALAPPDATA","TEMP","PUBLIC"]
 return "\n".join([f"USERPROFILE={home}"]+[f"{k}={os.environ.get(k,'')}" for k in keys])
TOOL={"name":"windows_user_profile","description":"Read-only Windows user profile paths and environment locations useful for file and app automation.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_user_profile}
