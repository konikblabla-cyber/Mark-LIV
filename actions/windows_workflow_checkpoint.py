"""Persist and inspect lightweight Windows workflow checkpoints."""
import json,platform
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
BASE=Path(__file__).resolve().parent.parent/"memory"; PATH=BASE/"workflow_checkpoints.json"
def _load():
 try:return json.loads(PATH.read_text(encoding="utf-8"))
 except Exception:return {}
def windows_workflow_checkpoint(parameters=None,**kwargs):
 p=parameters or {}; action=str(p.get("action","list")).lower(); data=_load()
 if action=="list": return json.dumps(data,ensure_ascii=False)
 name=str(p.get("name") or "").strip()
 if not name:return "Missing checkpoint name."
 if action=="save":
  BASE.mkdir(parents=True,exist_ok=True); data[name]=str(p.get("state","")); PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8"); return f"Checkpoint saved: {name}"
 if action=="get": return str(data.get(name,"Checkpoint not found."))
 if action=="remove":
  if name in data: del data[name]; PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
  return f"Checkpoint removed: {name}"
 return "Action must be list, save, get, or remove."
TOOL={"name":"windows_workflow_checkpoint","description":"Save, retrieve, list, or remove lightweight local checkpoints for multi-step Windows workflows.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"name":{"type":"STRING"},"state":{"type":"STRING"}}},"handler":windows_workflow_checkpoint}
