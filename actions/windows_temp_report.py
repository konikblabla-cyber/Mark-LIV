"""Windows temporary-file space inspection."""
import platform,os
from pathlib import Path
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_temp_report(parameters=None,**kwargs):
 p=parameters or {}; root=Path(os.environ.get("TEMP",str(Path.home()/ "AppData/Local/Temp"))); count=0; total=0
 try:
  for f in root.rglob("*"):
   if f.is_file():
    try:total+=f.stat().st_size;count+=1
    except OSError:pass
 except OSError:pass
 return f"Temp: {root}\nFiles: {count}\nApprox size: {total/1073741824:.2f} GB"
TOOL={"name":"windows_temp_report","description":"Read-only Windows TEMP folder report with file count and approximate disk usage.","parameters":{"type":"OBJECT","properties":{}},"handler=windows_temp_report}
