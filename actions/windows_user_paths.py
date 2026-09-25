"""Return common Windows user paths."""
import os,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_user_paths(parameters=None,**kwargs):
 h=os.environ.get("USERPROFILE","")
 v={"user":h,"desktop":os.path.join(h,"Desktop"),"documents":os.path.join(h,"Documents"),"downloads":os.path.join(h,"Downloads"),"appdata":os.environ.get("APPDATA",""),"localappdata":os.environ.get("LOCALAPPDATA","")}
 return "\n".join(f"{k}: {x}" for k,x in v.items())
TOOL={"name":"windows_user_paths","description":"Return common Windows profile and personal-folder paths.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_user_paths}
