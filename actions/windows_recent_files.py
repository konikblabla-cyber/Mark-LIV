"""Windows recent-files inspection."""
import platform,os
from pathlib import Path
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_recent_files(parameters=None,**kwargs):
 p=parameters or {}; root=Path(os.environ.get("USERPROFILE",str(Path.home())))/"Recent"; n=max(1,min(int(p.get("count",30)),100))
 if not root.exists():return "Recent folder not found."
 rows=[]
 for f in root.iterdir():
  try: rows.append((f.stat().st_mtime,f.name))
  except OSError:pass
 rows.sort(reverse=True)
 return "\n".join(x[1] for x in rows[:n]) or "No recent items."
TOOL={"name":"windows_recent_files","description":"Read-only list of recent Windows shell items from the current user's Recent folder.","parameters":{"type":"OBJECT","properties":{"count":{"type":"INTEGER"}},"required":["count"]},"handler=windows_recent_files}
