from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", BASE_DIR / "data" / "images"))
METADATA_PATH = Path(os.getenv("METADATA_PATH", BASE_DIR / "data" / "metadata.json"))
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
