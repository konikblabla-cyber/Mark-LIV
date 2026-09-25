"""Bounded local permanent task history."""
import json,platform,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"memory";FILE=ROOT/"task_history.json"
def _load():
 ROOT.mkdir(exist_ok=True)
 try:return json.loads(FILE.read_text(encoding="utf-8"))
 except:return []
def permanent_history(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {};a=str(p.get("action","list")).lower();d=_load()
 if a=="add":
  text=str(p.get("text","")).strip()
  if not text:return "History text is required."
  d.append({"time":int(time.time()),"text":text});d=d[-500:]
  FILE.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8");return "History entry saved."
 if a=="clear":
  FILE.write_text("[]",encoding="utf-8");return "Task history cleared."
 try:n=int(p.get("limit",20))
 except (TypeError,ValueError):n=20
 n=max(1,min(n,100))
 return "\n".join(f"- {x['text']}" for x in d[-n:] if isinstance(x,dict) and "text" in x) or "No task history."
TOOL={"name":"permanent_history","description":"Persist bounded local task history across Mark-LIV restarts; list or clear it.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"text":{"type":"STRING"},"limit":{"type":"INTEGER"}}},"handler":permanent_history}
