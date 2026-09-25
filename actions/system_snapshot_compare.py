"""Compare two Windows system snapshots stored locally."""
import json,platform
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
STORE=Path(__file__).resolve().parents[1]/"memory"/"system_snapshot.json"
def system_snapshot_compare(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","compare")).lower()
 if a=="save":
  snap=p.get("snapshot")
  if not isinstance(snap,dict):return "snapshot object required."
  STORE.parent.mkdir(parents=True,exist_ok=True); STORE.write_text(json.dumps(snap,indent=2),encoding="utf-8"); return "System snapshot saved."
 if a=="show":
  if not STORE.exists():return "No saved snapshot."
  return STORE.read_text(encoding="utf-8")[:12000]
 if a=="compare":
  if not STORE.exists():return "No saved snapshot."
  try:old=json.loads(STORE.read_text(encoding="utf-8")); new=p.get("snapshot")
  except Exception:return "Saved snapshot is invalid."
  if not isinstance(new,dict):return "snapshot object required."
  keys=sorted(set(old)|set(new)); changes=[f"{k}: {old.get(k)!r} -> {new.get(k)!r}" for k in keys if old.get(k)!=new.get(k)]
  return "\n".join(changes) or "No changes detected."
 return "Unknown snapshot action."
TOOL={"name":"system_snapshot_compare","description":"Save, show, or compare a local Windows system snapshot to detect configuration or hardware changes.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"snapshot":{"type":"OBJECT"}},"required":["action"]},"handler":system_snapshot_compare}
