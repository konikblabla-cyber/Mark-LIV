"""Local study notes for Mark-LIV."""
import json,platform
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"memory";FILE=ROOT/"study_notes.json"
def _load():
    ROOT.mkdir(parents=True,exist_ok=True)
    try:
        data=json.loads(FILE.read_text(encoding="utf-8"))
        return data if isinstance(data,dict) else {}
    except Exception:return {}
def study_notes(parameters=None,**kwargs):
    if platform.system()!="Windows": return "Windows-only action."
    p=parameters or {};a=str(p.get("action","list")).lower().strip();d=_load()
    if a=="set":
        k=str(p.get("topic","")).strip();v=str(p.get("note","")).strip()
        if not k or not v:return "Topic and note are required."
        d[k]=v;FILE.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8");return f"Saved note: {k}"
    if a=="get":
        k=str(p.get("topic","")).strip();return d.get(k,f"No note for: {k}")
    if a=="remove":
        k=str(p.get("topic","")).strip()
        if k in d:
            del d[k];FILE.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8");return f"Removed note: {k}"
        return f"No note for: {k}"
    return "\n".join(f"- {k}: {v}" for k,v in list(d.items())[-200:]) or "No study notes."
TOOL={"name":"study_notes","description":"Persist, read, list and remove local study notes by topic.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"topic":{"type":"STRING"},"note":{"type":"STRING"}}},"handler":study_notes}
