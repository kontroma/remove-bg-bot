import asyncio
import gc
import io
import logging

import onnxruntime as ort
from PIL import Image
from rembg import new_session, remove

logger = logging.getLogger(__name__)

_session = None


def _build_sess_options(intra_threads: int) -> ort.SessionOptions:
    opts = ort.SessionOptions()
    # Limit threads — each thread allocates its own memory arena.
    opts.intra_op_num_threads = intra_threads
    opts.inter_op_num_threads = 1
    # Don't cache memory allocation patterns; trades tiny speed for lower baseline RAM.
    opts.enable_mem_pattern = False
    opts.enable_mem_reuse = True
    return opts


def _load_model(model_name: str, intra_threads: int) -> None:
    global _session
    logger.info("Loading rembg model '%s' (intra_threads=%d)...", model_name, intra_threads)
    sess_opts = _build_sess_options(intra_threads)
    _session = new_session(model_name, sess_opts=sess_opts, providers=["CPUExecutionProvider"])
    logger.info("Model loaded successfully.")


def _resize_if_needed(image: Image.Image, max_side: int) -> Image.Image:
    """Downscale *image* so its longest side is at most *max_side* pixels.

    Keeps the original if it's already small enough.
    """
    w, h = image.size
    longest = max(w, h)
    if longest <= max_side:
        return image
    scale = max_side / longest
    new_size = (round(w * scale), round(h * scale))
    logger.debug("Resizing %dx%d → %dx%d before inference.", w, h, *new_size)
    return image.resize(new_size, Image.LANCZOS)


def _remove_background(image_bytes: bytes, max_side: int) -> bytes:
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    input_image = _resize_if_needed(input_image, max_side)

    output_image: Image.Image = remove(input_image, session=_session)

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    result = buf.getvalue()

    # Help CPython return memory to the OS sooner after each request.
    del input_image, output_image, buf
    gc.collect()

    return result


async def preload_model(model_name: str, intra_threads: int) -> None:
    await asyncio.to_thread(_load_model, model_name, intra_threads)


async def remove_background(image_bytes: bytes, max_side: int) -> bytes:
    return await asyncio.to_thread(_remove_background, image_bytes, max_side)
