"""Autonomous storage advisor: find likely removable files, then delete only after UI confirmation."""
from __future__ import annotations
import json
import os
import platform
from collections import defaultdict
from pathlib import Path
from core import confirm

SKIP_DIRS = {
    "AppData", "Windows", "Program Files", "Program Files (x86)",
    "$Recycle.Bin", "System Volume Information", ".git", "node_modules",
    "__pycache__", "venv", ".venv"
}
SAFE_EXTS = {".tmp", ".log", ".bak", ".old", ".dmp", ".crdownload", ".part"}
INSTALLER_EXTS = {".exe", ".msi", ".iso"}
MEDIA_EXTS = {".jpg",".jpeg",".png",".webp",".gif",".mp4",".mov",".mkv",".avi"}
DOC_EXTS = {".doc",".docx",".pdf",".txt",".xlsx",".pptx",".py",".ps1",".zip",".7z",".rar"}

def _candidate_score(p: Path, size: int) -> int:
    n = p.name.lower()
    ext = p.suffix.lower()
    score = min(50, int(size / (1024**3) * 10))
    if ext in SAFE_EXTS: score += 70
    if any(x in n for x in ("temp","cache","crash","dump","old","backup")): score += 25
    if ext in INSTALLER_EXTS: score += 18
    if ext in MEDIA_EXTS: score += 5
    if ext in DOC_EXTS: score -= 35
    if any(x in n for x in ("important","school","project","work","invoice","config","save")): score -= 100
    return score

def _scan(root: Path, limit: int = 30000):
    rows=[]; seen=0
    for base, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in files:
            if seen >= limit: return rows
            seen += 1
            try:
                p=Path(base)/name
                if not p.is_file(): continue
                s=p.stat()
                if s.st_size < 5*1024*1024: continue
                score=_candidate_score(p,s.st_size)
                if score >= 15:
                    rows.append({"path":str(p),"size_mb":round(s.st_size/1048576,1),"score":score})
            except (OSError,PermissionError): pass
    return rows

def storage_cleanup_advisor(parameters=None, **kwargs):
    if platform.system() != "Windows": return "Windows-only action."
    p=parameters or {}
    root=Path(str(p.get("root") or Path.home())).expanduser()
    if not root.is_dir(): return f"Directory not found: {root}"
    try: limit=max(1000,min(int(p.get("limit",30)),100))
    except (TypeError,ValueError): limit=30
    rows=_scan(root)
    rows.sort(key=lambda x:(-x["score"],-x["size_mb"]))
    top=rows[:limit]
    if not top: return "Nie znalazłem oczywistych kandydatów do bezpiecznego usunięcia."
    total=sum(x["size_mb"] for x in top)
    lines=[f"Znalazłem {len(top)} kandydatów, razem około {total:.1f} MB:"]
    for i,x in enumerate(top,1):
        lines.append(f"{i}. {x['path']} ({x['size_mb']} MB, score={x['score']})")
    return "\n".join(lines)

def storage_cleanup_execute(parameters=None, **kwargs):
    if platform.system() != "Windows": return "Windows-only action."
    p=parameters or {}
    raw=p.get("paths") or []
    if isinstance(raw,str):
        try: raw=json.loads(raw)
        except Exception: raw=[x.strip() for x in raw.splitlines() if x.strip()]
    paths=[Path(str(x)).expanduser() for x in raw if str(x).strip()]
    if not paths: return "No files selected."
    safe=[]
    for path in paths[:100]:
        try:
            if path.is_file() and path.stat().st_size >= 0:
                safe.append(path)
        except OSError: pass
    if not safe: return "No valid files selected."
    total=sum(x.stat().st_size for x in safe)
    detail="\n".join(f"- {x} ({x.stat().st_size/1048576:.1f} MB)" for x in safe)
    def run():
        deleted=0
        for x in safe:
            try: x.unlink(); deleted += 1
            except OSError: pass
        return f"Usunięto {deleted}/{len(safe)} plików, zwolniono około {total/1048576:.1f} MB."
    return confirm.request(
        key="storage_cleanup:delete",
        title=f"Usuń {len(safe)} wybranych plików?",
        detail=detail,
        run=run,
    )

TOOL = {
    "name":"storage_cleanup_advisor",
    "description":"Autonomicznie analizuje dysk i wybiera prawdopodobnie zbędne duże pliki; nigdy nie usuwa ich bez osobnego potwierdzenia.",
    "parameters":{"type":"OBJECT","properties":{
        "root":{"type":"STRING","description":"Folder to analyze; default is the user's home folder."},
        "limit":{"type":"INTEGER","description":"Maximum number of candidates to report."}
    }},
    "handler":storage_cleanup_advisor,
}
