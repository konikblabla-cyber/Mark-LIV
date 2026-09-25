"""Local study quiz bank."""
import json,platform
from pathlib import Path
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
ROOT=Path(__file__).resolve().parents[1]/"memory";FILE=ROOT/"study_quiz.json"
def _load():
 ROOT.mkdir(exist_ok=True)
 try:return json.loads(FILE.read_text(encoding="utf-8"))
 except:return []
def study_quiz(parameters=None,**kwargs):
 p=parameters or {};a=str(p.get("action","list")).lower();d=_load()
 if a=="add":
  q=str(p.get("question","")).strip();ans=str(p.get("answer","")).strip()
  if not q or not ans:return "Question and answer are required."
  d.append({"question":q,"answer":ans});FILE.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8");return f"Added question #{len(d)}."
 if a=="list":
  return "\n".join(f"{i+1}. {x['question']}" for i,x in enumerate(d)) or "No quiz questions."
 if a=="answer":
  try:i=int(p.get("number",0))-1
  except:return "Invalid question number."
  return d[i]["answer"] if 0<=i<len(d) else "Question not found."
 return "Actions: add, list, answer."
TOOL={"name":"study_quiz","description":"Maintain a local study question bank and retrieve answers on request.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"question":{"type":"STRING"},"answer":{"type":"STRING"},"number":{"type":"INTEGER"}}},"handler":study_quiz}
