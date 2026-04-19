import os
import logging
import asyncio
from flask import Flask, request, jsonify
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Update, CallbackQuery, Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from enum import Enum
from typing import Dict, List, Optional

# ========== ГЛОБАЛЬНЫЙ EVENT LOOP ==========
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# ========== КОНФИГУРАЦИЯ ==========
BOT_TOKEN = os.environ.get('BOT_TOKEN')
MANAGER_USERNAME = os.environ.get('MANAGER_USERNAME', '@Lobin24')
DEFAULT_LANGUAGE = os.environ.get('DEFAULT_LANGUAGE', 'DE')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '').rstrip('/')
WEBHOOK_PATH = '/webhook'

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set!")
if not WEBHOOK_URL:
    raise Exception("WEBHOOK_URL not set!")

# ========== НАСТРОЙКА ЛОГОВ ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== ЯЗЫКИ ==========
class Language(Enum):
    DE = "deutsch"
    EN = "english"
    RU = "russian"

# Тексты на всех языках
TEXTS = {
    Language.DE: {
        "welcome": "🌿 Willkommen in unserem Cannabis-Shop! 🌿\n\nWir bieten eine große Auswahl an hochwertigen Sorten für Sie.",
        "catalog": "📚 KATALOG",
        "select_category": "📂 Wählen Sie eine Kategorie:",
        "sativa": "🌿 SATIVA",
        "indica": "🌸 INDICA",
        "hybrid": "🔀 HYBRID",
        "all": "📚 ALLE SORTEN",
        "select_plant": "🌿 Wählen Sie eine Sorte:",
        "order_button": "📦 ZUM MANAGER",
        "no_plants": "🌿 In dieser Kategorie gibt es noch keine Sorten",
        "back_to_categories": "↩️ Zurück zu Kategorien",
        "back_to_menu": "🏠 Hauptmenü",
        "contact_manager": "📦 MANAGER KONTAKTIEREN"
    },
    Language.EN: {
        "welcome": "🌿 Welcome to our Cannabis Shop! 🌿\n\nWe offer a wide selection of high-quality strains for you.",
        "catalog": "📚 CATALOG",
        "select_category": "📂 Select a category:",
        "sativa": "🌿 SATIVA",
        "indica": "🌸 INDICA",
        "hybrid": "🔀 HYBRID",
        "all": "📚 ALL STRAINS",
        "select_plant": "🌿 Select a strain:",
        "order_button": "📦 CONTACT MANAGER",
        "no_plants": "🌿 No strains in this category yet",
        "back_to_categories": "↩️ Back to categories",
        "back_to_menu": "🏠 Main menu",
        "contact_manager": "📦 CONTACT MANAGER"
    },
    Language.RU: {
        "welcome": "🌿 Добро пожаловать в наш Cannabis-магазин! 🌿\n\nМы предлагаем широкий выбор качественных сортов.",
        "catalog": "📚 КАТАЛОГ",
        "select_category": "📂 Выберите категорию:",
        "sativa": "🌿 САТИВА",
        "indica": "🌸 ИНДИКА",
        "hybrid": "🔀 ГИБРИД",
        "all": "📚 ВСЕ СОРТА",
        "select_plant": "🌿 Выберите сорт:",
        "order_button": "📦 К МЕНЕДЖЕРУ",
        "no_plants": "🌿 В этой категории пока нет сортов",
        "back_to_categories": "↩️ Назад к категориям",
        "back_to_menu": "🏠 В главное меню",
        "contact_manager": "📦 СВЯЗАТЬСЯ С МЕНЕДЖЕРОМ"
    }
}

def get_text(lang: Language, key: str) -> str:
    return TEXTS.get(lang, TEXTS[Language.DE]).get(key, key)

# ========== КЛАВИАТУРЫ ==========
def get_main_menu_keyboard(lang: Language) -> types.ReplyKeyboardMarkup:
    """Главное меню с тремя кнопками"""
    catalog_text = get_text(lang, "catalog")
    order_text = get_text(lang, "order_button")

    # Кнопка смены языка
    if lang == Language.DE:
        lang_text = "🌐 ENGLISH / РУССКИЙ"
    elif lang == Language.EN:
        lang_text = "🌐 DEUTSCH / РУССКИЙ"
    else:
        lang_text = "🌐 DEUTSCH / ENGLISH"

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=catalog_text)],           # Первый ряд: Каталог
            [types.KeyboardButton(text=order_text),             # Второй ряд: К менеджеру
             types.KeyboardButton(text=lang_text)]              # и Сменить язык
        ],
        resize_keyboard=True
    )
    return keyboard

def get_category_keyboard(lang: Language) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=get_text(lang, "sativa"))],
            [types.KeyboardButton(text=get_text(lang, "indica"))],
            [types.KeyboardButton(text=get_text(lang, "hybrid"))],
            [types.KeyboardButton(text=get_text(lang, "all"))],
            [types.KeyboardButton(text=get_text(lang, "back_to_menu"))]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_plants_keyboard(plants, lang: Language) -> types.ReplyKeyboardMarkup:
    buttons = []
    for plant in plants:
        buttons.append([types.KeyboardButton(text=plant.display_name)])
    buttons.append([types.KeyboardButton(text=get_text(lang, "back_to_categories"))])

    return types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )

def get_plant_navigation_keyboard(lang: Language, current_index: int, total: int, category: str, plant_id: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if current_index > 0:
        builder.add(types.InlineKeyboardButton(text=f"◀️ {current_index}", callback_data=f"prev_{category}_{current_index}"))
    else:
        builder.add(types.InlineKeyboardButton(text="◀️ --", callback_data="empty"))

    builder.add(types.InlineKeyboardButton(text=f"{current_index + 1}/{total}", callback_data="empty"))

    if current_index < total - 1:
        builder.add(types.InlineKeyboardButton(text=f"{current_index + 2} ▶️", callback_data=f"next_{category}_{current_index}"))
    else:
        builder.add(types.InlineKeyboardButton(text="-- ▶️", callback_data="empty"))

    builder.adjust(3)

    builder.row(
        types.InlineKeyboardButton(text=get_text(lang, "back_to_categories"), callback_data=f"back_cat_{category}"),
        types.InlineKeyboardButton(text=get_text(lang, "back_to_menu"), callback_data="back_menu")
    )

    builder.row(types.InlineKeyboardButton(text=get_text(lang, "contact_manager"), callback_data="contact_manager"))

    return builder.as_markup()

def get_back_to_menu_keyboard(lang: Language) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=get_text(lang, "back_to_menu"))]],
        resize_keyboard=True
    )

# ========== КЛАСС РАСТЕНИЯ ==========
class Plant:
    def __init__(self, plant_id: str, display_name: str, price: float, thc: float, cbd: float, genetics: str, description: str, photo_num: int):
        self.id = plant_id
        self.display_name = display_name
        self.price = price
        self.thc = thc
        self.cbd = cbd
        self.genetics = genetics
        self.description = description
        self.photo_num = photo_num

    def get_full_info_text(self, lang: Language) -> str:
        return f"""*{self.display_name}*

💰 *Preis:* {self.price:.2f} €/g
🔥 *THC:* {self.thc}% | *CBD:* {self.cbd}%
🌱 *Genetik:* {self.genetics}

📝 {self.description}"""

    def get_photo_path(self) -> Optional[str]:
        photo_path = f"photos/{self.photo_num}.jpg"
        if os.path.exists(photo_path):
            return photo_path
        return None

# ========== ДАННЫЕ РАСТЕНИЙ ==========
PLANTS = [
    Plant("gs1", "🧄 Garlic Skittlez", 4.25, 30.0, 1.0, "Hybrid", "Eufloria 30/1 GSZ - Ein intensives Aroma mit knoblauchartigen Noten.", 1),
    Plant("mc1", "🍪 Minty Cookies", 4.25, 27.0, 1.0, "Hybrid", "enua 27/1 PS3 CA MYC - Frische Minze mit süßen Cookie-Noten.", 2),
    Plant("cd1", "🍩 Crispy Doughnut", 4.25, 25.0, 1.0, "Indica dominant", "enua 25/1 CDG CA - Wie ein frischer Doughnut.", 3),
    Plant("sm1", "🖍️ Scented Marker", 5.95, 33.0, 1.0, "Indica dominant", "420 Evolution 33/1 CA SCM - Intensives Aroma.", 4),
    Plant("pk1", "🌸 Pink Kush", 4.25, 24.5, 1.0, "Hybrid", "enua 27/1 PS3 PNK - Sanft und entspannend.", 5),
    Plant("mn1", "🍬 Munyunz", 4.25, 27.0, 1.0, "Sativa dominant", "Remexian 27/1 GJY MUN - Energiegeladen.", 6),
    Plant("pc1", "🟣 Purple Churro", 5.20, 27.0, 1.0, "Indica dominant", "Eufloria 27/1 PCH - Süß und würzig.", 7),
    Plant("zr1", "🍬 Zlush Runtz", 5.20, 30.0, 1.0, "Indica dominant", "Eufloria 30/1 ZRU - Fruchtig und stark.", 8),
    Plant("ok1", "🌲 OG Kush", 4.25, 22.0, 1.0, "Hybrid", "Slouu 22/1 PS3 CA OGK - Klassiker mit Kiefernaroma.", 9),
    Plant("ww1", "🕷️ White Widow", 4.90, 18.0, 1.0, "Hybrid", "Weeco 1A 18/1 WW - Legendärer Strain.", 10),
    Plant("mo1", "🍡 Marshmallow OG", 5.20, 27.0, 1.0, "Indica dominant", "Eufloria 27/1 MOG - Sanft und süß.", 11),
    Plant("pf1", "🍍 Pineapple Fruz", 5.95, 27.0, 1.0, "Sativa dominant", "420 Evolution 27/1 CA PEX - Tropischer Geschmack.", 12),
    Plant("ss1", "🍬 Sweet San Valley", 5.60, 30.0, 1.0, "Indica dominant", "enua SSV CA 30/1 - Sanft und entspannend.", 13),
    Plant("pg1", "🍍 Pineapple God", 5.20, 25.0, 1.0, "Sativa dominant", "Huala 25/1 CA POG - Exotisch und fruchtig.", 14),
    Plant("jf1", "🌴 Jungle Fumes", 7.45, 36.0, 1.0, "Sativa dominant", "enua 36/1 JGF CA - Extrem potent.", 15),
    Plant("co1", "🍪 Cookies OG", 5.30, 30.0, 0.9, "Hybrid", "TRUU GT 30:01 - Süß und erdig.", 16),
    Plant("aa1", "🧠 Amsterdam Amnesia", 8.20, 24.0, 0.9, "Sativa", "Cannamedical Sativa Forte NM - Klassischer Geschmack.", 17),
    Plant("sl1", "🍋 Super Lemon G", 6.00, 5.6, 6.8, "Sativa", "420 Balanced Basic PT SLG - Ausgewogen und zitronig.", 18),
    Plant("pr1", "🌧️ Purple Rain", 4.10, 21.2, 0.9, "Sativa", "Weeco Duke 20/1 - Fruchtig und entspannend.", 19),
    Plant("fc1", "💎 First Class Funk", 8.50, 28.0, 0.9, "Indica dominant", "Demecan CRAFT FCF 28:01 - Premium Qualität.", 20),
    Plant("ls1", "🍋 Lemon Slushie", 6.98, 20.0, 1.0, "Sativa", "Cannamedical Sativa Classic - Erfrischend und belebend.", 21),
    Plant("wt1", "💍 Wedding Tree", 8.30, 24.0, 0.9, "Sativa", "Cannamedical Sativa forte NM - Elegant und stark.", 22),
    Plant("pc2", "🍑 Peach Chementine", 7.20, 30.0, 0.9, "Hybrid", "420 Evolution 30/1 CA PCH - Fruchtig und potent.", 23),
]

# ========== ХРАНИЛИЩА ПОЛЬЗОВАТЕЛЕЙ ==========
user_languages: Dict[int, Language] = {}
user_category_cache: Dict[int, Dict[str, List[Plant]]] = {}

def get_user_language(user_id: int) -> Language:
    if user_id in user_languages:
        return user_languages[user_id]
    return Language.DE

def get_plants_by_category(user_id: int, category: str, lang: Language) -> List[Plant]:
    if user_id not in user_category_cache:
        user_category_cache[user_id] = {}

    cache_key = f"{category}_{lang.value}"
    if cache_key not in user_category_cache[user_id]:
        if category == "sativa":
            filtered = [p for p in PLANTS if "sativa" in p.genetics.lower()]
        elif category == "indica":
            filtered = [p for p in PLANTS if "indica" in p.genetics.lower()]
        elif category == "hybrid":
            filtered = [p for p in PLANTS if "hybrid" in p.genetics.lower()]
        else:
            filtered = PLANTS.copy()
        user_category_cache[user_id][cache_key] = filtered

    return user_category_cache[user_id][cache_key]

# ========== ИНИЦИАЛИЗАЦИЯ БОТА ==========
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# ========== ХЕНДЛЕРЫ ==========
@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    await message.answer(get_text(lang, "welcome"), reply_markup=get_main_menu_keyboard(lang))

@dp.message(lambda m: m.text in [get_text(Language.DE, "catalog"), get_text(Language.EN, "catalog"), get_text(Language.RU, "catalog")])
async def show_categories(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    await message.answer(get_text(lang, "select_category"), reply_markup=get_category_keyboard(lang))

@dp.message(lambda m: m.text in [get_text(Language.DE, "sativa"), get_text(Language.EN, "sativa"), get_text(Language.RU, "sativa")])
async def show_sativa(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    plants = get_plants_by_category(user_id, "sativa", lang)
    if not plants:
        await message.answer(get_text(lang, "no_plants"))
        return
    await message.answer(get_text(lang, "select_plant"), reply_markup=get_plants_keyboard(plants, lang))

@dp.message(lambda m: m.text in [get_text(Language.DE, "indica"), get_text(Language.EN, "indica"), get_text(Language.RU, "indica")])
async def show_indica(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    plants = get_plants_by_category(user_id, "indica", lang)
    if not plants:
        await message.answer(get_text(lang, "no_plants"))
        return
    await message.answer(get_text(lang, "select_plant"), reply_markup=get_plants_keyboard(plants, lang))

@dp.message(lambda m: m.text in [get_text(Language.DE, "hybrid"), get_text(Language.EN, "hybrid"), get_text(Language.RU, "hybrid")])
async def show_hybrid(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    plants = get_plants_by_category(user_id, "hybrid", lang)
    if not plants:
        await message.answer(get_text(lang, "no_plants"))
        return
    await message.answer(get_text(lang, "select_plant"), reply_markup=get_plants_keyboard(plants, lang))

@dp.message(lambda m: m.text in [get_text(Language.DE, "all"), get_text(Language.EN, "all"), get_text(Language.RU, "all")])
async def show_all(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    plants = get_plants_by_category(user_id, "all", lang)
    await message.answer(get_text(lang, "select_plant"), reply_markup=get_plants_keyboard(plants, lang))

@dp.message(lambda m: m.text in [get_text(Language.DE, "order_button"), get_text(Language.EN, "order_button"), get_text(Language.RU, "order_button")])
async def contact_manager(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    manager_clean = MANAGER_USERNAME.replace("@", "")
    manager_link = f"https://t.me/{manager_clean}"
    text = f"📦 Kontaktieren Sie den Manager:\n👉 {manager_link}\n\nOder schreiben Sie direkt: {MANAGER_USERNAME}"
    await message.answer(text, reply_markup=get_back_to_menu_keyboard(lang))

@dp.message(lambda m: m.text in ["🌐 ENGLISH / РУССКИЙ", "🌐 DEUTSCH / РУССКИЙ", "🌐 DEUTSCH / ENGLISH"])
async def show_language_menu(message: Message):
    """Показать меню выбора языка"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🇩🇪 DEUTSCH")],
            [types.KeyboardButton(text="🇬🇧 ENGLISH")],
            [types.KeyboardButton(text="🇷🇺 РУССКИЙ")],
            [types.KeyboardButton(text=get_text(lang, "back_to_menu"))]
        ],
        resize_keyboard=True
    )

    await message.answer("🌐 Wählen Sie Ihre Sprache / Select your language / Выберите язык:", reply_markup=keyboard)

@dp.message(lambda m: m.text in ["🇩🇪 DEUTSCH", "🇬🇧 ENGLISH", "🇷🇺 РУССКИЙ"])
async def set_language(message: Message):
    """Установка выбранного языка"""
    user_id = message.from_user.id

    if message.text == "🇩🇪 DEUTSCH":
        user_languages[user_id] = Language.DE
    elif message.text == "🇬🇧 ENGLISH":
        user_languages[user_id] = Language.EN
    else:
        user_languages[user_id] = Language.RU

    # Очищаем кэш при смене языка
    if user_id in user_category_cache:
        del user_category_cache[user_id]

    lang = get_user_language(user_id)
    await message.answer(get_text(lang, "welcome"), reply_markup=get_main_menu_keyboard(lang))

@dp.message(lambda m: m.text in [get_text(Language.DE, "back_to_categories"), get_text(Language.EN, "back_to_categories"), get_text(Language.RU, "back_to_categories")])
async def back_to_categories(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    await message.answer(get_text(lang, "select_category"), reply_markup=get_category_keyboard(lang))

@dp.message(lambda m: m.text in [get_text(Language.DE, "back_to_menu"), get_text(Language.EN, "back_to_menu"), get_text(Language.RU, "back_to_menu")])
async def back_to_menu(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    if user_id in user_category_cache:
        del user_category_cache[user_id]
    await message.answer(get_text(lang, "welcome"), reply_markup=get_main_menu_keyboard(lang))

@dp.message()
async def show_plant_details(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    plant_name = message.text

    for plant in PLANTS:
        if plant.display_name == plant_name:
            if "sativa" in plant.genetics.lower():
                category = "sativa"
            elif "indica" in plant.genetics.lower():
                category = "indica"
            else:
                category = "hybrid"

            plants = get_plants_by_category(user_id, category, lang)
            index = next((i for i, p in enumerate(plants) if p.id == plant.id), 0)

            text = plant.get_full_info_text(lang)
            photo_path = plant.get_photo_path()
            keyboard = get_plant_navigation_keyboard(lang, index, len(plants), category, plant.id)

            if photo_path and os.path.exists(photo_path):
                try:
                    photo = FSInputFile(photo_path)
                    await message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)
                except Exception as e:
                    logger.error(f"Photo error: {e}")
                    await message.answer(text, reply_markup=keyboard)
            else:
                await message.answer(text, reply_markup=keyboard)
            return

    await message.answer(get_text(lang, "select_category"), reply_markup=get_category_keyboard(lang))

@dp.callback_query(lambda c: c.data.startswith("prev_"))
async def nav_prev(callback: CallbackQuery):
    data = callback.data.split("_")
    category = data[1]
    current_index = int(data[2])
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    plants = get_plants_by_category(user_id, category, lang)

    if current_index > 0:
        new_index = current_index - 1
        plant = plants[new_index]
        text = plant.get_full_info_text(lang)
        photo_path = plant.get_photo_path()
        keyboard = get_plant_navigation_keyboard(lang, new_index, len(plants), category, plant.id)

        if photo_path and os.path.exists(photo_path):
            try:
                photo = FSInputFile(photo_path)
                await callback.message.delete()
                await callback.message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)
            except Exception as e:
                logger.error(f"Photo error: {e}")
                await callback.message.edit_text(text, reply_markup=keyboard)
        else:
            await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("next_"))
async def nav_next(callback: CallbackQuery):
    data = callback.data.split("_")
    category = data[1]
    current_index = int(data[2])
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    plants = get_plants_by_category(user_id, category, lang)

    if current_index < len(plants) - 1:
        new_index = current_index + 1
        plant = plants[new_index]
        text = plant.get_full_info_text(lang)
        photo_path = plant.get_photo_path()
        keyboard = get_plant_navigation_keyboard(lang, new_index, len(plants), category, plant.id)

        if photo_path and os.path.exists(photo_path):
            try:
                photo = FSInputFile(photo_path)
                await callback.message.delete()
                await callback.message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)
            except Exception as e:
                logger.error(f"Photo error: {e}")
                await callback.message.edit_text(text, reply_markup=keyboard)
        else:
            await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("back_cat_"))
async def back_to_categories_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    await callback.message.delete()
    await callback.message.answer(get_text(lang, "select_category"), reply_markup=get_category_keyboard(lang))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_menu")
async def back_to_menu_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    if user_id in user_category_cache:
        del user_category_cache[user_id]
    await callback.message.delete()
    await callback.message.answer(get_text(lang, "welcome"), reply_markup=get_main_menu_keyboard(lang))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "contact_manager")
async def contact_manager_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    manager_clean = MANAGER_USERNAME.replace("@", "")
    manager_link = f"https://t.me/{manager_clean}"
    text = f"📦 Kontaktieren Sie den Manager:\n👉 {manager_link}\n\nOder schreiben Sie direkt: {MANAGER_USERNAME}"
    await callback.message.answer(text, reply_markup=get_back_to_menu_keyboard(lang))
    await callback.answer()

@dp.callback_query(lambda c: c.data == "empty")
async def empty_callback(callback: CallbackQuery):
    await callback.answer()

# ========== FLASK ПРИЛОЖЕНИЕ ==========
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return jsonify({"status": "Bot is running", "webhook_url": WEBHOOK_URL})

@flask_app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@flask_app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    """Обработчик вебхука"""
    try:
        update_data = request.get_json()
        if not update_data:
            return jsonify({"error": "No data"}), 400

        update = Update.model_validate(update_data)

        # Создаём новый event loop для каждого запроса
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(dp.feed_update(bot, update))
        new_loop.close()

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

# ========== ЗАПУСК ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting Flask server on port {port}")
    flask_app.run(host='0.0.0.0', port=port, debug=False)