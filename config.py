import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20 MB
REMBG_MODEL: str = "isnet-general-use"
LOG_FILE: str = "bot.log"
LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT: int = 3
# Resize input image to this side length before inference to cap peak RAM usage.
# 1024 gives good quality while keeping memory predictable.
MAX_IMAGE_SIDE: int = int(os.getenv("MAX_IMAGE_SIDE", "1024"))
# Number of ONNX intra-op threads (each thread owns a memory arena).
ONNX_INTRA_THREADS: int = int(os.getenv("ONNX_INTRA_THREADS", "2"))
