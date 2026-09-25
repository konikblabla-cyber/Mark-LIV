"""Local study progress tracker."""
import json,platform
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
ROOT=Path(__file__).resolve().parents[1]/"memory";FILE=ROOT/"study_progress.json"
def _load():
 ROOT.mkdir(exist_ok=True)
 try:return json.loads(FILE.read_text(encoding="utf-8"))
 except:return {}
def study_progress(parameters=None,**kwargs):
 p=parameters or {};a=str(p.get("action","list")).lower();d=_load()
 if a=="set":
  k=str(p.get("topic","")).strip()
  try:v=max(0,min(100,int(p.get("percent",0))))
  except:return "Percent must be an integer."
  if not k:return "Topic is required."
  d[k]=v;FILE.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8");return f"{k}: {v}%"
 if a=="get":
  k=str(p.get("topic","")).strip();return f"{k}: {d[k]}%" if k in d else f"No progress for: {k}"
 return "\n".join(f"- {k}: {v}%" for k,v in d.items()) or "No study progress."
TOOL={"name":"study_progress","description":"Persist and report local study progress percentages by topic.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"topic":{"type":"STRING"},"percent":{"type":"INTEGER"}}},"handler":study_progress}
