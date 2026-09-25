"""Bounded directory snapshot/compare action (cross-platform)."""
import json
import os
from pathlib import Path

def _snap(root, limit=3000):
    out = {}
    try:
        for base, dirs, files in os.walk(root):
            dirs[:] = dirs[:100]
            for n in files[:500]:
                q = Path(base) / n
                try:
                    out[str(q.relative_to(root))] = (q.stat().st_size, q.stat().st_mtime_ns)
                except OSError:
                    pass
                if len(out) >= limit:
                    return out
    except OSError:
        pass
    return out

def directory_change_compare(parameters=None, **kwargs):
    p = parameters or {}
    action = str(p.get("action", "compare")).lower().strip()
    root = Path(str(p.get("path", "")).strip()).expanduser()

    if action == "snapshot":
        if not root.is_dir():
            return "Directory not found."
        return json.dumps(_snap(root), ensure_ascii=False)[:30000]

    if action == "compare":
        if not root.is_dir():
            return "Directory not found."
        old = p.get("snapshot")
        if not isinstance(old, dict):
            return "snapshot object required."
        new = _snap(root)
        added = sorted(set(new) - set(old))
        removed = sorted(set(old) - set(new))
        changed = sorted(
            k for k in set(new) & set(old)
            if tuple(new[k]) != tuple(old[k])
        )
        return json.dumps(
            {"added": added[:200], "removed": removed[:200], "changed": changed[:200]},
            ensure_ascii=False, indent=2
        )

    return "Unknown directory_change_compare action."

TOOL = {
    "name": "directory_change_compare",
    "description": "Create a bounded directory snapshot or compare a previous snapshot to detect added, removed, and modified files.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {"type": "STRING"},
            "path": {"type": "STRING"},
            "snapshot": {"type": "OBJECT"},
        },
        "required": ["action"],
    },
    "handler": directory_change_compare,
}
