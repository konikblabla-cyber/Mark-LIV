"""Persistent Windows workspace configuration."""
import json,os,platform
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
ROOT=Path(__file__).resolve().parents[1]; STORE=ROOT/"memory"/"workspaces.json"
DEFAULT={"gaming":["steam.exe"],"school":["notepad.exe"],"coding":["code.exe"]}
def _load():
 STORE.parent.mkdir(parents=True,exist_ok=True)
 try:return {**DEFAULT,**json.loads(STORE.read_text(encoding="utf-8"))}
 except Exception:return dict(DEFAULT)
def persistent_workspaces(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","list")).lower(); data=_load()
 if a=="list": return json.dumps(data,ensure_ascii=False,indent=2)
 name=str(p.get("name","")).strip().lower()
 if a=="set":
  apps=p.get("apps",[])
  if not name or not isinstance(apps,list) or not all(isinstance(x,str) and x.strip() for x in apps): return "Workspace name and app list required."
  data[name]=[x.strip() for x in apps[:20]]
  STORE.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8"); return f"Saved workspace: {name}"
 if a=="remove":
  if name not in data:return "Workspace not found."
  del data[name]; STORE.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8"); return f"Removed workspace: {name}"
 return "Unknown workspace action."
TOOL={"name":"persistent_workspaces","description":"Manage persistent named Windows workspaces in local memory: list, set app lists, or remove a workspace.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"name":{"type":"STRING"},"apps":{"type":"ARRAY","items":{"type":"STRING"}}},"required":["action"]},"handler":persistent_workspaces}
