"""Advanced, conservative storage analysis for Mark-LIV.
Scans the selected drive/folder, explains why files are candidates, and never
deletes anything by itself.
"""
from __future__ import annotations
import os
import platform
from pathlib import Path
from datetime import datetime, timezone
import psutil
from send2trash import send2trash

SKIP_DIRS = {
    "AppData", "Windows", "Program Files", "Program Files (x86)",
    "$Recycle.Bin", "System Volume Information", ".git", "node_modules",
    "__pycache__", "venv", ".venv", "site-packages"
}
DISPOSABLE_EXTS = {".tmp", ".log", ".bak", ".old", ".dmp", ".crdownload", ".part", ".cache"}
INSTALLER_EXTS = {".exe", ".msi", ".iso"}
USER_DOC_EXTS = {".doc",".docx",".pdf",".txt",".xlsx",".pptx",".py",".ps1",".json",".zip",".7z",".rar"}
MEDIA_EXTS = {".jpg",".jpeg",".png",".webp",".gif",".mp4",".mov",".mkv",".avi"}

def _reason(path: Path, size: int, age_days: float) -> tuple[int, list[str]]:
    n, ext = path.name.lower(), path.suffix.lower()
    score = min(35, int(size / (1024**3) * 8))
    reasons = []
    if ext in DISPOSABLE_EXTS:
        score += 70; reasons.append("plik tymczasowy/log/kopia techniczna")
    if any(x in n for x in ("temp", "cache", "crash", "dump")):
        score += 28; reasons.append("nazwa wskazuje na dane tymczasowe")
    if any(x in n for x in ("old", "backup", "bak")):
        score += 20; reasons.append("wygląda na starą kopię")
    if age_days >= 180 and ext in DISPOSABLE_EXTS:
        score += 25; reasons.append(f"niezmieniany od {int(age_days)} dni")
    if ext in INSTALLER_EXTS:
        score += 12; reasons.append("instalator/obraz ISO")
    if ext in MEDIA_EXTS:
        score -= 8
    if ext in USER_DOC_EXTS:
        score -= 45
    if any(x in n for x in ("important","school","project","work","invoice","config","save")):
        score -= 140; reasons.append("nazwa sugeruje ważne dane")
    if not reasons:
        reasons.append("duży plik, ale brak mocnego sygnału że jest zbędny")
    return score, reasons

def _scan(root: Path, max_files: int = 50000, min_mb: float = 5.0):
    rows = []
    seen = 0
    cutoff = 5 * 1024 * 1024
    for base, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in files:
            if seen >= max_files:
                return rows
            seen += 1
            try:
                p = Path(base) / name
                s = p.stat()
                if not p.is_file() or s.st_size < max(cutoff, int(min_mb * 1048576)):
                    continue
                age = max(0.0, (datetime.now(timezone.utc).timestamp() - s.st_mtime) / 86400)
                score, reasons = _reason(p, s.st_size, age)
                if score >= 35:
                    rows.append({"path": str(p), "size_mb": round(s.st_size/1048576, 1),
                                 "age_days": int(age), "score": score, "reasons": reasons})
            except (OSError, PermissionError):
                continue
    return rows

def storage_cleanup_advisor(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    p = parameters or {}
    raw_root = str(p.get("root") or "")
    if raw_root:
        root = Path(raw_root).expanduser()
    else:
        root = Path(os.environ.get("SystemDrive", "C:") + "\\")
    if not root.is_dir():
        return f"Directory not found: {root}"
    try:
        limit = max(1, min(int(p.get("limit", 30)), 100))
    except (TypeError, ValueError):
        limit = 30
    try:
        min_mb = max(1.0, min(float(p.get("min_mb", 5)), 10240))
    except (TypeError, ValueError):
        min_mb = 5.0
    usage = psutil.disk_usage(str(root))
    rows = _scan(root, min_mb=min_mb)
    rows.sort(key=lambda x: (-x["score"], -x["size_mb"]))
    top = rows[:limit]
    lines = [
        f"Dysk: {root}",
        f"Zajęte: {usage.percent:.1f}% | wolne: {usage.free/1073741824:.1f} GB | razem: {usage.total/1073741824:.1f} GB",
        f"Znalazłem {len(top)} kandydatów (to rekomendacje, nie automatyczne usuwanie)."
    ]
    for i, x in enumerate(top, 1):
        why = "; ".join(x["reasons"])
        lines.append(f"{i}. {x['path']} | {x['size_mb']:.1f} MB | {x['age_days']} dni | {why}")
    if not top:
        lines.append("Brak wystarczająco mocnych kandydatów.")
    return "\n".join(lines)


def cleanup_confirmed(parameters=None, **kwargs):
    """Move explicitly selected cleanup candidates to the Windows Recycle Bin."""
    p = parameters or {}
    raw = p.get("paths") or []
    if isinstance(raw, str):
        raw = [raw]
    paths = [str(x).strip() for x in raw if str(x).strip()][:20]
    if not paths:
        return "No cleanup paths supplied."
    safe = []
    for raw_path in paths:
        path = Path(raw_path).expanduser()
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        safe.append(path)
    if not safe:
        return "No safe cleanup candidates found."
    from core import confirm
    names = ", ".join(p.name for p in safe[:5])
    return confirm.request(
        key="cleanup:" + str(abs(hash("|".join(map(str, safe))))),
        title="Move selected files to Recycle Bin",
        detail=f"JARVIS will move {len(safe)} selected file(s) to the Recycle Bin: {names}",
        run=lambda: _move_to_trash(safe),
    )


def _move_to_trash(paths):
    moved = 0
    failed = []
    for path in paths:
        try:
            send2trash(str(path))
            moved += 1
        except Exception as exc:
            failed.append(f"{path.name}: {str(exc)[:100]}")
    result = f"Moved {moved} file(s) to the Recycle Bin."
    if failed:
        result += " Failed: " + "; ".join(failed[:5])
    return result

TOOL = [
    {
    "name": "storage_cleanup_confirmed",
    "description": "Move explicitly selected cleanup candidates to the Windows Recycle Bin. Always requires human confirmation.",
    "parameters": {"type":"OBJECT","properties":{"paths":{"type":"ARRAY","items":{"type":"STRING"}}},"required":["paths"]},
    "handler": cleanup_confirmed,
    },
    {
    "name": "storage_cleanup_advisor",
    "description": "Zaawansowanie analizuje zajętość dysku i wybiera tylko mocne, wyjaśnione kandydatury do czyszczenia; niczego nie usuwa.",
    "parameters": {"type":"OBJECT","properties":{
        "root":{"type":"STRING","description":"Dysk/folder do analizy; domyślnie dysk systemowy."},
        "limit":{"type":"INTEGER","description":"Maksymalnie 100 kandydatów, domyślnie 30."},
        "min_mb":{"type":"NUMBER","description":"Minimalny rozmiar pliku w MB, domyślnie 5."}
    }},
    "handler": storage_cleanup_advisor,
    },
]
