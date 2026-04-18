import asyncio
import logging
import sys
import os
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update

# Настройка логов
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN не найден!")
    sys.exit(1)

MANAGER_USERNAME = os.environ.get('MANAGER_USERNAME', '@Lobin24')
DEFAULT_LANGUAGE = os.environ.get('DEFAULT_LANGUAGE', 'RU')

# --- ИНИЦИАЛИЗАЦИЯ БОТА ---
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# --- ИМПОРТЫ ВАШИХ МОДУЛЕЙ ---
# (Скопируйте сюда импорты и обработчики из вашего старого bot.py)
# from language import Language, get_text
# from plants_data import get_all_plants, get_plants_by_genetics_type
# from keyboards import ...

# ========== ВАШИ ОБРАБОТЧИКИ (ОСТАЮТСЯ БЕЗ ИЗМЕНЕНИЙ) ==========
# ... (весь ваш код с @dp.message, который мы написали ранее) ...
# =================================================================

# --- FLASK ПРИЛОЖЕНИЕ ДЛЯ ВЕБХУКА ---
app = Flask(__name__)

@app.route('/')
def index():
    return "🌿 Бот работает!"

@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        update_data = await request.get_json()
        update = Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return "OK", 200
    except Exception as e:
        logging.error(f"Ошибка в вебхуке: {e}")
        return "ERROR", 500

# --- ЗАПУСК ---
if __name__ == "__main__":
    # Этот блок не используется на Render
    app.run()