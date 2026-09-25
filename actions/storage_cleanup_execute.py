"""Delete a user-approved set of files behind the real UI confirmation gate."""
from __future__ import annotations
import json, platform
from pathlib import Path
from core import confirm

def storage_cleanup_execute(parameters=None, **kwargs):
    if platform.system() != "Windows": return "Windows-only action."
    raw=(parameters or {}).get("paths") or []
    if isinstance(raw,str):
        try: raw=json.loads(raw)
        except Exception: raw=[x.strip() for x in raw.splitlines() if x.strip()]
    paths=[Path(str(x)).expanduser() for x in raw if str(x).strip()][:100]
    safe=[]
    for p in paths:
        try:
            if p.is_file(): safe.append(p)
        except OSError: pass
    if not safe: return "No valid files selected."
    total=sum(p.stat().st_size for p in safe)
    detail="\n".join(f"- {p} ({p.stat().st_size/1048576:.1f} MB)" for p in safe)
    def run():
        deleted=0
        for p in safe:
            try: p.unlink(); deleted+=1
            except OSError: pass
        return f"Usunięto {deleted}/{len(safe)} plików, zwolniono około {total/1048576:.1f} MB."
    return confirm.request(key="storage_cleanup:delete",title=f"Usuń {len(safe)} wybranych plików?",detail=detail,run=run)

TOOL={"name":"storage_cleanup_execute","description":"Usuń dokładnie wskazane pliki po prawdziwym potwierdzeniu użytkownika w interfejsie.","parameters":{"type":"OBJECT","properties":{"paths":{"type":"ARRAY","items":{"type":"STRING"}}},"required":["paths"]},"handler":storage_cleanup_execute}
