"""Windows file attribute inspection."""
import platform,os
from pathlib import Path
def file_attributes(parameters=None,**kwargs):
 if platform.system()!="Windows": return "file_attributes is available only on Windows."
 p=parameters or {}; path=Path(str(p.get("path","")))
 if not path.exists():return "Path not found."
 st=path.stat(); attrs=[]
 for flag,name in [(0x1,"READONLY"),(0x2,"HIDDEN"),(0x4,"SYSTEM"),(0x10,"DIRECTORY"),(0x20,"ARCHIVE")]:
  try:
   if st.st_file_attributes & flag:attrs.append(name)
  except AttributeError:pass
 return f"{path}\nAttributes: {', '.join(attrs) or 'NORMAL'}\nSize: {st.st_size} bytes"
TOOL={"name":"file_attributes","description":"Read-only Windows file/folder attribute and size inspection.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}},"required":["path"]},"handler":file_attributes}
