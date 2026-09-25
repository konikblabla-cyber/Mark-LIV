"""Persistent Windows process watch configuration."""
import json,platform
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
STORE=Path(__file__).resolve().parents[1]/"memory"/"watched_processes.json"
def process_watch_persist(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","list")).lower(); STORE.parent.mkdir(parents=True,exist_ok=True)
 try:data=json.loads(STORE.read_text(encoding="utf-8"))
 except Exception:data=[]
 data=[x for x in data if isinstance(x,str)][:100]
 name=str(p.get("process","")).strip()
 if a=="list":return "\n".join(data) or "No persistent watched processes."
 if a=="add":
  if not name or len(name)>128:return "Valid executable name required."
  if name.lower() not in {x.lower() for x in data}:data.append(name)
 elif a=="remove":data=[x for x in data if x.lower()!=name.lower()]
 else:return "Unknown process_watch_persist action."
 STORE.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8"); return f"Saved {len(data)} watched processes."
TOOL={"name":"process_watch_persist","description":"Persist the list of Windows process executables Mark-LIV should monitor across restarts.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"process":{"type":"STRING"}},"required":["action"]},"handler":process_watch_persist}
