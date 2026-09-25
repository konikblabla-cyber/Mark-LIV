"""Windows-only file operations for Mark-LIV."""
import os, platform, shutil
from pathlib import Path
WIN=platform.system()=="Windows"

def _path(v):
    p=Path(str(v or "").strip().strip('"')).expanduser()
    return p

def file_control(parameters=None, **kwargs):
    if not WIN: return "This action is Windows-only."
    p=parameters or {}; a=str(p.get("action","")).lower().strip()
    src=_path(p.get("source") or p.get("path")); dst=_path(p.get("destination") or p.get("target"))
    try:
        if a in ("file_search","search_files"):
            root=_path(p.get("root") or p.get("directory") or ".")
            pattern=str(p.get("pattern") or "*")
            if not root.exists(): return f"Directory not found: {root}"
            out=[] 
            for x in root.rglob(pattern):
                if x.is_file():
                    out.append(str(x))
                    if len(out)>=200: break
            return "\n".join(out) or "No matching files found."
        if a in ("folder_create","create_folder"):
            dst.mkdir(parents=True,exist_ok=True); return f"Folder created: {dst}"
        if a in ("file_copy","copy_file"):
            shutil.copy2(src,dst); return f"Copied: {src} -> {dst}"
        if a in ("file_move","move_file"):
            shutil.move(str(src),str(dst)); return f"Moved: {src} -> {dst}"
        if a in ("file_rename","rename_file"):
            src.rename(dst); return f"Renamed: {src} -> {dst}"
        if a in ("file_delete","delete_file"):
            src.unlink(); return f"Deleted: {src}"
        if a in ("folder_delete","delete_folder"):
            shutil.rmtree(src); return f"Deleted folder: {src}"
        if a in ("file_info","file_metadata"):
            s=src.stat(); return f"path={src}\nsize={s.st_size}\nmodified={s.st_mtime}\nreadonly={not os.access(src,os.W_OK)}"
        return "Unknown file action."
    except Exception as e: return f"File operation failed: {e}"

TOOL={"name":"file_control","description":"Windows file operations: search, create folder, copy, move, rename, delete files/folders, inspect metadata.","input_schema":{"type":"object","properties":{"action":{"type":"string"},"path":{"type":"string"},"source":{"type":"string"},"destination":{"type":"string"},"root":{"type":"string"},"pattern":{"type":"string"}},"required":["action"]}}
