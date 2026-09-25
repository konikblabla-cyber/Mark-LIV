"""Windows-only file operations for Mark-LIV."""
import os, platform, shutil
from pathlib import Path
WIN=platform.system()=="Windows"

def _path(v):
    p=Path(str(v or "").strip().strip('"')).expanduser()
    return p


def _important_index_path() -> Path:
    p = Path(__file__).resolve().parent.parent / "memory" / "important_files.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def _score_important_file(path: Path) -> int:
    name, suffix = path.name.lower(), path.suffix.lower()
    score = 40 if any(k in name for k in ("important","backup","project","school","work","document","invoice","config","save")) else 0
    return score + (15 if suffix in {".docx",".xlsx",".pptx",".pdf",".txt",".md",".json",".py",".ps1",".zip",".7z",".rar"} else 0)

def _build_important_index(root: Path, max_files=1000, max_scan_gb=50.0) -> str:
    max_files=max(1,min(int(max_files),10000)); max_bytes=max(1.0,min(float(max_scan_gb),200.0))*1024**3
    found=[]; scanned=0
    for base,dirs,files in os.walk(root,topdown=True):
        dirs[:]=[d for d in dirs if d not in {"$Recycle.Bin","System Volume Information"}]
        for name in files:
            try:
                p=Path(base)/name; size=p.stat().st_size; scanned+=size; found.append((_score_important_file(p),str(p),size))
            except (OSError,PermissionError): continue
            if scanned>=max_bytes: break
        if scanned>=max_bytes: break
    found.sort(key=lambda x:(-x[0],x[1].casefold())); found=found[:max_files]
    lines=["# Mark-LIV important file index","# Paths only; file contents are not stored here.",f"# Root: {root}",f"# Scan limit: {max_scan_gb:g} GB",""]
    lines.extend(f"{a}\t{b}\t{c} bytes" for a,b,c in found)
    out=_important_index_path(); out.write_text("\n".join(lines)+"\n",encoding="utf-8")
    return f"Indexed {len(found)} important file paths in {out}; scanned {scanned/1024**3:.2f} GB."

def _important_lookup(name: str) -> str:
    idx=_important_index_path()
    if not idx.exists(): return "Important file index does not exist yet. Run important_files_index first."
    needle=str(name).strip().casefold()
    if not needle: return "File name is required."
    matches=[x for x in idx.read_text(encoding="utf-8",errors="replace").splitlines() if "\t" in x and needle in x.casefold()]
    return "\n".join(matches[:50]) or f"No indexed important file matches '{name}'."

def file_control(parameters=None, **kwargs):
    if not WIN: return "This action is Windows-only."
    p=parameters or {}; a=str(p.get("action","")).lower().strip()
    src=_path(p.get("source") or p.get("path")); dst=_path(p.get("destination") or p.get("target"))
    try:
        if a in ("important_files_index","index_important_files"):
            root=_path(p.get("root") or p.get("directory") or str(Path.home()))
            return _build_important_index(root,p.get("max_files",1000),p.get("max_scan_gb",50)) if root.is_dir() else f"Directory not found: {root}"

        if a in ("important_file_lookup","lookup_important_file"):
            return _important_lookup(p.get("name") or p.get("query") or "")

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
        if a in ("file_read","read_file"):
            if not src.exists(): return f"File not found: {src}"
            if src.stat().st_size > 2_000_000: return "File is too large for direct reading."
            return src.read_text(encoding="utf-8",errors="replace")
        if a in ("file_write","write_file"):
            if not dst and src: dst=src
            if not dst: return "Destination path is required."
            dst.parent.mkdir(parents=True,exist_ok=True)
            dst.write_text(str(p.get("content","")),encoding="utf-8")
            return f"Written: {dst}"
        if a in ("zip_create","archive_create"):
            if not src.exists(): return f"Path not found: {src}"
            base=str(dst or src.with_suffix(""))
            shutil.make_archive(base,"zip",root_dir=str(src.parent),base_dir=src.name)
            return f"Archive created: {base}.zip"
        if a in ("zip_extract","archive_extract"):
            if not src.is_file(): return f"Archive not found: {src}"
            target=dst or src.with_suffix("")
            target.mkdir(parents=True,exist_ok=True)
            shutil.unpack_archive(str(src),str(target),"zip")
            return f"Archive extracted to: {target}"
        if a in ("file_hash","hash_file"):
            import hashlib
            if not src.is_file(): return f"File not found: {src}"
            h=hashlib.sha256()
            with src.open("rb") as f:
                for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
            return h.hexdigest()
        if a in ("file_info","file_metadata"):
            s=src.stat(); return f"path={src}\nsize={s.st_size}\nmodified={s.st_mtime}\nreadonly={not os.access(src,os.W_OK)}"
        return "Unknown file action."
    except Exception as e: return f"File operation failed: {e}"

TOOL={"name":"file_control","description":"Windows file operations plus important file indexing: build a ranked important_files.txt path index (up to 200 GB scan limit) and look up indexed paths by name.","parameters":{"type":"OBJECT","properties":{"action":{"type":"string"},"path":{"type":"string"},"source":{"type":"string"},"destination":{"type":"string"},"root":{"type":"string"},"pattern":{"type":"string"},"name":{"type":"string"},"max_files":{"type":"integer"},"max_scan_gb":{"type":"number"},"content":{"type":"string"}},"required":["action"]}}
