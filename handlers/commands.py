from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

START_TEXT = (
    "👋 Привет! Я бот для удаления фона с фотографий.\n\n"
    "Просто отправь мне изображение — и я верну его с прозрачным фоном в формате PNG.\n\n"
    "📎 Для лучшего качества отправляй файл как <b>документ</b> (без сжатия).\n"
    "📷 Обычные фото тоже принимаются.\n\n"
    "Используй /help для подробной справки."
)

HELP_TEXT = (
    "ℹ️ <b>Как пользоваться ботом</b>\n\n"
    "1. Отправь фото как <b>документ</b> — максимальное качество, без сжатия Telegram.\n"
    "2. Или отправь обычное <b>фото</b> — Telegram слегка сожмёт его, но результат будет хорошим.\n\n"
    "<b>Ограничения:</b>\n"
    "• Максимальный размер файла — 20 МБ\n"
    "• Поддерживаемые форматы: JPEG, PNG, WEBP, BMP, TIFF\n\n"
    "<b>Результат</b> всегда приходит в формате PNG с прозрачным фоном, "
    "отправленным как документ — так прозрачность сохраняется.\n\n"
    "<b>Команды:</b>\n"
    "/start — начать работу\n"
    "/help — эта справка"
)


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(START_TEXT, parse_mode="HTML")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, parse_mode="HTML")
