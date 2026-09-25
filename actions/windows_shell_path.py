"""Resolve common Windows special folders."""
import os,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
F={"desktop":"USERPROFILE/Desktop","documents":"USERPROFILE/Documents","downloads":"USERPROFILE/Downloads","pictures":"USERPROFILE/Pictures","videos":"USERPROFILE/Videos","music":"USERPROFILE/Music","appdata":"APPDATA","localappdata":"LOCALAPPDATA","temp":"TEMP"}
def windows_shell_path(parameters=None,**kwargs):
 k=str((parameters or {}).get("name","")).lower()
 if k not in F:return "Unknown folder."
 key,sub=F[k].split("/",1) if "/" in F[k] else ("","")
 base=os.environ.get(key,"") if key else ""
 path=os.path.join(base,sub) if base else os.environ.get(k.upper(),"")
 return os.path.abspath(path)
TOOL={"name":"windows_shell_path","description":"Resolve common Windows user special folders such as Desktop, Downloads, Documents and AppData.","parameters":{"type":"OBJECT","properties":{"name":{"type":"STRING"}},"required":["name"]},"handler":windows_shell_path}
