import sys
import os
import asyncio
import logging
from aiogram.client.session.aiohttp import AiohttpSession

# Настройка логов для отладки
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update

# --- Конфигурация ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN не найден в переменных окружения!")
    # Создаем заглушку приложения, чтобы сайт просто показывал ошибку
    app = Flask(__name__)
    @app.route('/')
    def index(): return "Ошибка: BOT_TOKEN не настроен", 500
    application = app
    sys.exit(1)

# --- Инициализация бота ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Обработчики ---
@dp.message()
async def echo_all(message: types.Message):
    """Тестовый обработчик на все сообщения"""
    await message.answer("✅ Бот работает! Ваше сообщение получено.")

# --- Flask приложение ---
app = Flask(__name__)

@app.route('/')
def index():
    return "🌿 Бот для продажи Cannabis работает! 🚀"

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Принимаем обновления от Telegram"""
    try:
        update_data = await request.get_json()
        logging.info(f"Получен вебхук: {update_data.get('message', {}).get('text')}")
        update = Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return "OK", 200
    except Exception as e:
        logging.error(f"Ошибка в вебхуке: {e}")
        return "ERROR", 500

# --- Настройка вебхука при старте (для PythonAnywhere) ---
async def setup_webhook():
    """Устанавливает вебхук один раз при запуске"""
    webhook_url = 'https://blkmkl.pythonanywhere.com/webhook'
    result = await bot.set_webhook(url=webhook_url)
    if result:
        logging.info(f"✅ Вебхук успешно установлен на {webhook_url}")
    else:
        logging.error(f"❌ Ошибка установки вебхука на {webhook_url}")

# Запускаем настройку вебхука в фоновом потоке
def start_background_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(setup_webhook())
    loop.close()

import threading
threading.Thread(target=start_background_loop).start()

# Это для совместимости с ожиданиями PythonAnywhere
application = app