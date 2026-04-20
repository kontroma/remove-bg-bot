import io
import logging
from typing import Optional

from aiogram import Bot, Router
from aiogram.types import BufferedInputFile, Document, Message, PhotoSize

from config import MAX_FILE_SIZE, MAX_IMAGE_SIDE
from services import bg_remover

logger = logging.getLogger(__name__)
router = Router()

_UNSUPPORTED_MIME = {
    "image/gif",
    "image/svg+xml",
    "video/mp4",
}


async def _download_file(bot: Bot, file_id: str) -> Optional[bytes]:
    file = await bot.get_file(file_id)
    buf = io.BytesIO()
    await bot.download_file(file.file_path, buf)  # type: ignore[arg-type]
    return buf.getvalue()


async def _process(message: Message, bot: Bot, file_id: str, filename: str) -> None:
    status = await message.answer("⏳ Обрабатываю...")

    try:
        image_bytes = await _download_file(bot, file_id)
        if image_bytes is None:
            raise RuntimeError("Не удалось скачать файл")

        result_bytes = await bg_remover.remove_background(image_bytes, MAX_IMAGE_SIDE)

        output = BufferedInputFile(result_bytes, filename=filename)
        await message.answer_document(output, caption="✅ Готово! Фон удалён.")
    except Exception as exc:
        logger.exception("Failed to process image for user %s", message.from_user and message.from_user.id)
        await message.answer(
            f"❌ Не удалось обработать изображение: <code>{exc}</code>\n\n"
            "Убедись, что это обычное изображение (JPEG, PNG, WEBP и т.д.) и попробуй ещё раз.",
            parse_mode="HTML",
        )
    finally:
        await status.delete()


@router.message(lambda m: m.photo is not None)
async def handle_photo(message: Message, bot: Bot) -> None:
    photo: PhotoSize = message.photo[-1]  # largest available size

    if photo.file_size and photo.file_size > MAX_FILE_SIZE:
        await message.answer("❌ Файл слишком большой. Максимальный размер — 20 МБ.")
        return

    await _process(message, bot, photo.file_id, "result.png")


@router.message(lambda m: m.document is not None)
async def handle_document(message: Message, bot: Bot) -> None:
    doc: Document = message.document  # type: ignore[assignment]

    if doc.mime_type in _UNSUPPORTED_MIME:
        await message.answer(
            "❌ Этот тип файла не поддерживается. Отправь изображение (JPEG, PNG, WEBP и т.д.)."
        )
        return

    if not (doc.mime_type or "").startswith("image/"):
        await message.answer("❌ Пожалуйста, отправь изображение, а не другой тип файла.")
        return

    if doc.file_size and doc.file_size > MAX_FILE_SIZE:
        await message.answer("❌ Файл слишком большой. Максимальный размер — 20 МБ.")
        return

    base_name = (doc.file_name or "image").rsplit(".", 1)[0]
    await _process(message, bot, doc.file_id, f"{base_name}_no_bg.png")
