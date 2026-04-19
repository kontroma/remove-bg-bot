FROM python:3.11-slim

WORKDIR /app

# System deps for rembg / Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-download the rembg model into the image so the first request is fast.
# The model is stored in /root/.u2net inside the container.
RUN python - <<'EOF'
from rembg import new_session
new_session("isnet-general-use")
print("Model downloaded successfully.")
EOF

CMD ["python", "bot.py"]
