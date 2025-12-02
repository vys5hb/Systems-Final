import json
import hashlib
from pathlib import Path
from datetime import datetime
from PIL import Image
from .config import METADATA_PATH

def ensure_metadata_file():
    METADATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not METADATA_PATH.exists():
        METADATA_PATH.write_text("[]", encoding="utf-8")

def load_metadata():
    ensure_metadata_file()
    try:
        return json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

def save_metadata(entries):
    METADATA_PATH.write_text(json.dumps(entries, indent=2), encoding="utf-8")

def compute_file_hash(path: Path, chunk_size: int = 8192) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def extract_image_metadata(file_path: Path) -> dict:
    """Extract basic metadata from the stored image."""
    with Image.open(file_path) as img:
        width, height = img.size
        format_ = img.format
    stats = file_path.stat()

    return {
        "filename": file_path.name,
        "stored_path": str(file_path),
        "size_bytes": stats.st_size,
        "width": width,
        "height": height,
        "format": format_,
        "sha256": compute_file_hash(file_path),
        "uploaded_at": datetime.utcnow().isoformat() + "Z",
    }

def register_image(file_path: Path):
    """Main pipeline step: extract metadata and append to catalog."""
    entries = load_metadata()
    meta = extract_image_metadata(file_path)
    entries.append(meta)
    save_metadata(entries)
    return meta

