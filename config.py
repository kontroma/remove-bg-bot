import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20 MB
REMBG_MODEL: str = "isnet-general-use"
LOG_FILE: str = "bot.log"
LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT: int = 3
