"""Read-only directory comparison by relative paths and metadata."""
from pathlib import Path

def directory_compare(parameters=None, **kwargs):
    p = parameters or {}
    a = Path(str(p.get("left", ".")).strip()).expanduser()
    b = Path(str(p.get("right", ".")).strip()).expanduser()
    if not a.is_dir() or not b.is_dir():
        return "Both directories must exist."

    def snap(root):
        d = {}
        try:
            for f in root.rglob("*"):
                if f.is_file():
                    try:
                        d[str(f.relative_to(root))] = (
                            f.stat().st_size, f.stat().st_mtime_ns
                        )
                    except OSError:
                        pass
        except OSError:
            pass
        return d

    x, y = snap(a), snap(b)
    added = sorted(set(y) - set(x))
    removed = sorted(set(x) - set(y))
    changed = sorted(k for k in set(x) & set(y) if x[k] != y[k])
    return (
        f"Only left: {len(removed)}\n"
        f"Only right: {len(added)}\n"
        f"Changed: {len(changed)}\n\n"
        + ("\n".join(changed[:100]) or "No differing common files.")
    )

TOOL = {
    "name": "directory_compare",
    "description": "Read-only comparison of two directories by relative paths, sizes and modification times.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "left": {"type": "STRING"},
            "right": {"type": "STRING"},
        },
        "required": ["left", "right"],
    },
    "handler": directory_compare,
}
