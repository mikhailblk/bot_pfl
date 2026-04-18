import asyncio
import logging
import sys
import os
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Update

# --- Конфигурация ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN не найден!")
    sys.exit(1)

# --- Инициализация бота ---
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# ========== ВАШИ ОБРАБОТЧИКИ (скопируйте их сюда) ==========
# Вместо этого примера скопируйте сюда все ваши @dp.message и @dp.callback_query из вашего bot.py
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("✅ Бот работает! Ваше сообщение получено.")
# =========================================================

# --- Flask приложение ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"

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

# Эта строка нужна для gunicorn
application = app