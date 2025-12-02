import os
from pathlib import Path
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, send_from_directory
)
from werkzeug.utils import secure_filename
import logging
from .config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH
from .pipeline import register_image, load_metadata

def create_app():
    base_dir = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static"),
    )
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "ethanosecretkey")
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("app.log")]
    )

    def allowed_file(filename: str) -> bool:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @app.route("/")
    
    def index():
        images = load_metadata()
        return render_template("index.html", images=images)
    
    @app.route("/upload", methods=["POST"])
    
    def upload():
        if "image" not in request.files:
            flash("No file part in the request")
            return redirect(url_for("index"))
        file = request.files["image"]
        if file.filename == "":
            flash("No file selected")
            return redirect(url_for("index"))
        if not allowed_file(file.filename):
            flash("Unsupported file type")
            return redirect(url_for("index"))

        filename = secure_filename(file.filename)
        filename = f"{int(Path().stat().st_mtime_ns)}_{filename}"
        file_path = UPLOAD_DIR / filename
        file.save(file_path)
        meta = register_image(file_path)
        app.logger.info(
            "Stored image %s (%d bytes, %dx%d, %s)",
            meta["filename"],
            meta["size_bytes"],
            meta["width"],
            meta["height"],
            meta["format"],
        )
        flash("Image uploaded successfully!")
        return redirect(url_for("index"))
    
    @app.route("/images/<path:filename>")
    
    def serve_image(filename):
        return send_from_directory(UPLOAD_DIR, filename)

    @app.route("/health")
    
    def health():
        return {"status": "ok"}

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)

