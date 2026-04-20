FROM python:3.11-slim

# Reduce memory footprint:
# - OMP/OpenBLAS thread caps prevent each thread from allocating its own arena.
# - MALLOC_TRIM_THRESHOLD tells glibc to return freed memory to the OS promptly.
# - PYTHONUNBUFFERED keeps logs streaming without an extra buffer.
ENV OMP_NUM_THREADS=2 \
    OPENBLAS_NUM_THREADS=2 \
    MKL_NUM_THREADS=2 \
    MALLOC_TRIM_THRESHOLD_=65536 \
    PYTHONUNBUFFERED=1

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
