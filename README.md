# Remove BG Bot

Telegram-бот для удаления фона с изображений на основе [rembg](https://github.com/danielgatis/rembg) (модель `isnet-general-use`).

## Возможности

- Принимает фото (сжатые Telegram) и документы (без сжатия)
- Возвращает PNG с прозрачным фоном как документ
- Предзагружает ML-модель при старте — первый запрос не тормозит
- Ограничение файла: 20 МБ

## Требования

- Python 3.11+
- [BotFather](https://t.me/BotFather) — нужен `BOT_TOKEN`

## Установка и запуск локально

```bash
# 1. Клонируй репозиторий
git clone <repo-url>
cd remove-bg-bot

# 2. Создай виртуальное окружение
python3.11 -m venv .venv
source .venv/bin/activate

# 3. Установи зависимости
pip install -r requirements.txt

# 4. Скопируй .env и вставь токен
cp .env.example .env
# Отредактируй .env: BOT_TOKEN=<твой_токен>

# 5. Запусти
python bot.py
```

## Переменные окружения

| Переменная  | Описание                     | Обязательная |
|-------------|------------------------------|:------------:|
| `BOT_TOKEN` | Токен Telegram-бота (BotFather) | ✅ |

## Запуск через Docker

```bash
docker build -t remove-bg-bot .
docker run -d --env-file .env --name remove-bg-bot remove-bg-bot
```

> Модель `isnet-general-use` загружается в Docker-образ при сборке (`docker build`),
> поэтому старт контейнера быстрый.

## Структура проекта

```
.
├── bot.py                  # Точка входа
├── config.py               # Настройки из .env
├── handlers/
│   ├── commands.py         # /start, /help
│   └── photos.py           # Обработка фото и документов
├── services/
│   └── bg_remover.py       # Обёртка над rembg
├── requirements.txt
├── Dockerfile
├── .env.example
└── CLAUDE.md
```
