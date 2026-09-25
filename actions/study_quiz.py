"""Local study quiz bank."""
import json,platform
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"memory";FILE=ROOT/"study_quiz.json"
def _load():
    ROOT.mkdir(parents=True,exist_ok=True)
    try:
        data=json.loads(FILE.read_text(encoding="utf-8"))
        return data if isinstance(data,list) else []
    except Exception:return []
def study_quiz(parameters=None,**kwargs):
    if platform.system()!="Windows": return "Windows-only action."
    p=parameters or {};a=str(p.get("action","list")).lower().strip();d=_load()
    if a=="add":
        q=str(p.get("question","")).strip();ans=str(p.get("answer","")).strip()
        if not q or not ans:return "Question and answer are required."
        if len(d)>=500:return "Quiz bank limit reached (500 questions)."
        d.append({"question":q[:2000],"answer":ans[:4000]});FILE.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8");return f"Added question #{len(d)}."
    if a=="list":
        return "\n".join(f"{i+1}. {x.get('question','')}" for i,x in enumerate(d) if isinstance(x,dict)) or "No quiz questions."
    if a=="answer":
        try:i=int(p.get("number",0))-1
        except (TypeError,ValueError):return "Invalid question number."
        return d[i].get("answer","Answer unavailable.") if 0<=i<len(d) and isinstance(d[i],dict) else "Question not found."
    return "Actions: add, list, answer."
TOOL={"name":"study_quiz","description":"Maintain a local study question bank and retrieve answers on request.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"question":{"type":"STRING"},"answer":{"type":"STRING"},"number":{"type":"INTEGER"}}},"handler":study_quiz}
