FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/

RUN mkdir -p /app/data/images

ENV FLASK_APP=src.app
ENV PORT=8080
ENV UPLOAD_DIR=/app/data/images
ENV METADATA_PATH=/app/data/metadata.json

EXPOSE 8080

CMD ["python", "-m", "src.app"]
