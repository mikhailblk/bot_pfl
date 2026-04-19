import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла (для локальной разработки)
load_dotenv()

# Получаем переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_USERNAME = os.getenv("MANAGER_USERNAME", "@Lobin24")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "DE")

# Проверяем обязательные переменные
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables!")

# Опционально: проверяем формат MANAGER_USERNAME
if MANAGER_USERNAME and not MANAGER_USERNAME.startswith("@"):
    MANAGER_USERNAME = f"@{MANAGER_USERNAME}"