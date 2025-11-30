from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Where uploaded files go
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", BASE_DIR / "data" / "images"))

# Where our metadata catalog lives
METADATA_PATH = Path(os.getenv("METADATA_PATH", BASE_DIR / "data" / "metadata.json"))

# 10 MB upload limit
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
