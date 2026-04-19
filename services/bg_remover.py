import asyncio
import io
import logging
from PIL import Image
from rembg import new_session, remove

logger = logging.getLogger(__name__)

_session = None


def _load_model(model_name: str) -> None:
    global _session
    logger.info("Loading rembg model '%s'...", model_name)
    _session = new_session(model_name)
    logger.info("Model loaded successfully.")


def _remove_background(image_bytes: bytes) -> bytes:
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    output_image: Image.Image = remove(input_image, session=_session)
    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    return buf.getvalue()


async def preload_model(model_name: str) -> None:
    await asyncio.to_thread(_load_model, model_name)


async def remove_background(image_bytes: bytes) -> bytes:
    return await asyncio.to_thread(_remove_background, image_bytes)
