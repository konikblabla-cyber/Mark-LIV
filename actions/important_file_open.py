"""Open a file resolved from Mark-LIV's important-file index."""
import platform,os
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def important_file_open(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("name") or p.get("query") or "").strip().casefold()
 if not needle:return "File name is required."
 idx=Path(__file__).resolve().parent.parent/"memory"/"important_files.txt"
 if not idx.exists():return "Important file index does not exist. Run important_files_index first."
 matches=[]
 for line in idx.read_text(encoding="utf-8",errors="replace").splitlines():
  if "	" in line and needle in line.casefold():
   path=line.split("	",1)[1].rsplit("	",1)[0]
   if Path(path).is_file():matches.append(path)
 if not matches:return f"No indexed file matches '{needle}'."
 if len(matches)>1:return "Multiple matches:\n"+"\n".join(matches[:20])
 os.startfile(matches[0]); return f"Opened: {matches[0]}"
TOOL={"name":"important_file_open","description":"Windows-only: resolve one indexed important file by name and open it; ambiguous matches are returned without opening.","parameters":{"type":"OBJECT","properties":{"name":{"type":"STRING"}},"required":["name"]},"handler":important_file_open}
