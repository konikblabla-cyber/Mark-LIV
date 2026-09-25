"""Persistent Windows system snapshot compare."""
import json,platform
from pathlib import Path
STORE=Path(__file__).resolve().parents[1]/"memory"/"system_snapshot.json"
def system_snapshot_compare(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; a=str(p.get("action","show")).lower()
 if a=="save":
  snap=p.get("snapshot")
  if not isinstance(snap,dict): return "snapshot object required."
  STORE.parent.mkdir(parents=True,exist_ok=True); STORE.write_text(json.dumps(snap,indent=2),encoding="utf-8"); return "System snapshot saved."
 if not STORE.exists(): return "No saved snapshot."
 try: old=json.loads(STORE.read_text(encoding="utf-8"))
 except Exception: return "Saved snapshot is invalid."
 if a=="show": return json.dumps(old,ensure_ascii=False,indent=2)[:12000]
 if a=="compare":
  new=p.get("snapshot")
  if not isinstance(new,dict): return "snapshot object required."
  return "\n".join(f"{k}: {old.get(k)!r} -> {new.get(k)!r}" for k in sorted(set(old)|set(new)) if old.get(k)!=new.get(k)) or "No changes detected."
 return "Unknown system_snapshot_compare action."
TOOL={"name":"system_snapshot_compare","description":"Save, show, or compare a local Windows system snapshot.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"snapshot":{"type":"OBJECT"}},"required":["action"]},"handler":system_snapshot_compare}
