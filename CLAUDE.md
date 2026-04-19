# CLAUDE.md — Remove BG Bot

## Что это

Telegram-бот для удаления фона с фотографий.
- **Язык:** Python 3.11, async/await
- **Фреймворк:** aiogram 3.x
- **ML:** rembg (модель `isnet-general-use`) — запускается через `asyncio.to_thread`
- **Изображения:** Pillow

## Структура

```
bot.py                  # точка входа, polling
config.py               # переменные из .env
handlers/
  commands.py           # /start, /help
  photos.py             # photo + document handlers
services/
  bg_remover.py         # обёртка над rembg (preload + remove_background)
```

## Ключевые решения

- Модель загружается один раз при старте (`preload_model`) в `bot.py` — пользователи не ждут.
- Все вызовы rembg и Pillow идут через `asyncio.to_thread` — event loop не блокируется.
- Результат всегда PNG, отправляется как `document` — прозрачность не теряется.
- Лимит файла: 20 МБ (константа `MAX_FILE_SIZE` в `config.py`).
- Логирование: `RotatingFileHandler` → `bot.log` + stdout.

## Быстрый старт

```bash
cp .env.example .env  # добавь BOT_TOKEN
pip install -r requirements.txt
python bot.py
```

## Docker

```bash
docker build -t remove-bg-bot .   # модель загружается в образ
docker run -d --env-file .env --name remove-bg-bot remove-bg-bot
```
