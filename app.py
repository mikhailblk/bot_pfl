import asyncio
import logging
import os
from flask import Flask, request, jsonify
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Update

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')  # Обязательно добавить!

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set")
if not WEBHOOK_URL:
    raise Exception("WEBHOOK_URL not set")

# --- НАСТРОЙКА ЛОГОВ ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- ИНИЦИАЛИЗАЦИЯ ---
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# --- ОБРАБОТЧИКИ ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Бот работает через вебхук!")

# --- FLASK ---
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"status": "Bot is running", "webhook_url": WEBHOOK_URL})

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик вебхука (синхронный, т.к. Flask не async)"""
    try:
        # Получаем JSON из запроса
        update_data = request.get_json()

        if not update_data:
            logger.warning("Empty update data")
            return jsonify({"error": "No data"}), 400

        # Запускаем асинхронную обработку в цикле
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            update = Update.model_validate(update_data)
            loop.run_until_complete(dp.feed_update(bot, update))
        finally:
            loop.close()

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

# --- НАСТРОЙКА ВЕБХУКА ---
async def setup_webhook():
    """Установка вебхука при старте"""
    webhook_full_url = f"{WEBHOOK_URL}/webhook"
    logger.info(f"Setting webhook to: {webhook_full_url}")

    result = await bot.set_webhook(
        url=webhook_full_url,
        allowed_updates=["message", "callback_query"]
    )

    if result:
        logger.info("✅ Webhook set successfully!")
    else:
        logger.error("❌ Failed to set webhook")

    return result

def run_with_webhook():
    """Запуск Flask с настройкой вебхука"""
    port = int(os.environ.get('PORT', 10000))

    # Настраиваем вебхук перед запуском
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(setup_webhook())
    loop.close()

    # Запускаем Flask сервер
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

# Для совместимости с gunicorn
application = app

if __name__ == '__main__':
    run_with_webhook()