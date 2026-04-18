import asyncio
import logging
import os
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Update

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set")

# --- ИНИЦИАЛИЗАЦИЯ ---
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# --- ПРОСТОЙ ОБРАБОТЧИК ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Бот работает через вебхук!")

# --- FLASK ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"

@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        update = Update.model_validate(await request.json, context={"bot": bot})
        await dp.feed_update(bot, update)
        return "OK", 200
    except Exception as e:
        print(f"Error: {e}")
        return "ERROR", 500

application = app