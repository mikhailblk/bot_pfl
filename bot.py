import asyncio
import os
from typing import Dict, List

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from config import BOT_TOKEN, MANAGER_USERNAME, DEFAULT_LANGUAGE
from language import Language, get_text
from plants_data import get_all_plants, get_plants_by_genetics_type
from keyboards import (
    get_main_menu_keyboard,
    get_category_keyboard,
    get_plants_keyboard,
    get_back_to_categories_keyboard,
    get_back_to_menu_keyboard,
    get_plant_navigation_keyboard
)

# Инициализация бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# Хранилище языков пользователей
user_languages: Dict[int, Language] = {}

# Хранилище для кэширования списков растений по категориям
category_cache: Dict[int, Dict[str, List]] = {}


def get_user_language(user_id: int) -> Language:
    """Получить язык пользователя или язык по умолчанию"""
    if user_id in user_languages:
        return user_languages[user_id]
    lang_map = {"DE": Language.DE, "EN": Language.EN, "RU": Language.RU}
    return lang_map.get(DEFAULT_LANGUAGE, Language.DE)


def get_plants_for_category(user_id: int, category: str, lang: Language) -> List:
    """Получить список растений для категории с кэшированием"""
    cache_key = f"{user_id}_{category}_{lang.value}"

    if user_id not in category_cache:
        category_cache[user_id] = {}

    if cache_key not in category_cache[user_id]:
        if category == "sativa":
            plants = get_plants_by_genetics_type("sativa", lang)
        elif category == "indica":
            plants = get_plants_by_genetics_type("indica", lang)
        elif category == "hybrid":
            plants = get_plants_by_genetics_type("hybrid", lang)
        else:  # all
            plants = get_all_plants()

        category_cache[user_id][cache_key] = plants

    return category_cache[user_id][cache_key]


async def show_plant_by_index(message_or_callback, user_id: int, lang: Language,
                              category: str, plant_index: int, is_callback: bool = False):
    """Показать растение по индексу в категории"""

    plants = get_plants_for_category(user_id, category, lang)

    if plant_index < 0 or plant_index >= len(plants):
        return

    plant = plants[plant_index]
    text = plant.get_full_info_text(lang)
    photo_path = plant.get_photo_path()

    keyboard = get_plant_navigation_keyboard(lang, plant_index, len(plants), category, plant.id)

    if is_callback:
        callback = message_or_callback
        if photo_path and os.path.exists(photo_path):
            try:
                photo = FSInputFile(photo_path)
                await callback.message.delete()
                await callback.message.answer_photo(
                    photo=photo,
                    caption=text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Ошибка отправки фото: {e}")
                await callback.message.edit_text(
                    text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard
                )
        else:
            await callback.message.edit_text(
                text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboard
            )
        await callback.answer()
    else:
        message = message_or_callback
        if photo_path and os.path.exists(photo_path):
            try:
                photo = FSInputFile(photo_path)
                await message.answer_photo(
                    photo=photo,
                    caption=text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Ошибка отправки фото: {e}")
                await message.answer(
                    text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard
                )
        else:
            await message.answer(
                text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboard
            )

@dp.callback_query(lambda c: c.data == "contact_manager")
async def contact_manager_callback(callback: types.CallbackQuery):
    """Обработчик кнопки связи с менеджером в карточке товара"""
    user_id = callback.from_user.id
    lang = get_user_language(user_id)

    manager = MANAGER_USERNAME
    manager_clean = manager.replace("@", "")
    manager_link = f"https://t.me/{manager_clean}"

    if lang == Language.RU:
        text = f"📦 Нажмите на ссылку, чтобы связаться с менеджером:\n👉 {manager_link}\n\nИли напишите напрямую: {manager}"
    elif lang == Language.EN:
        text = f"📦 Click the link to contact the manager:\n👉 {manager_link}\n\nOr write directly: {manager}"
    else:
        text = f"📦 Klicken Sie auf den Link, um den Manager zu kontaktieren:\n👉 {manager_link}\n\nOder schreiben Sie direkt: {manager}"

    await callback.message.answer(text, reply_markup=get_back_to_menu_keyboard(lang))
    await callback.answer()  # Закрывает "бесконечную загрузку"

@dp.message(Command("start"))
async def start_command(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    welcome_text = get_text(lang, "welcome")
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(lang))


@dp.message(lambda message: message.text == "📚 KATALOG" or
                            message.text == "📚 CATALOG" or
                            message.text == "📚 КАТАЛОГ")
async def show_categories(message: Message):
    """Показать категории"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    await message.answer(
        get_text(lang, "select_category"),
        reply_markup=get_category_keyboard(lang)
    )


# Обработчики для категорий
@dp.message(lambda message: message.text in ["🌿 SATIVA", "🌿 САТИВА"])
async def show_sativa(message: Message):
    """Показать все сорта Сатива"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    plants = get_plants_for_category(user_id, "sativa", lang)

    if not plants:
        text = get_text(lang, "no_plants")
        await message.answer(text, reply_markup=get_back_to_categories_keyboard(lang))
        return

    await message.answer(
        get_text(lang, "select_plant"),
        reply_markup=get_plants_keyboard(plants, lang, show_back_to_categories=True)
    )


@dp.message(lambda message: message.text in ["🌸 INDICA", "🌸 ИНДИКА"])
async def show_indica(message: Message):
    """Показать все сорта Индика"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    plants = get_plants_for_category(user_id, "indica", lang)

    if not plants:
        text = get_text(lang, "no_plants")
        await message.answer(text, reply_markup=get_back_to_categories_keyboard(lang))
        return

    await message.answer(
        get_text(lang, "select_plant"),
        reply_markup=get_plants_keyboard(plants, lang, show_back_to_categories=True)
    )


@dp.message(lambda message: message.text in ["🔀 HYBRID", "🔀 ГИБРИД"])
async def show_hybrid(message: Message):
    """Показать все сорта Гибрид"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    plants = get_plants_for_category(user_id, "hybrid", lang)

    if not plants:
        text = get_text(lang, "no_plants")
        await message.answer(text, reply_markup=get_back_to_categories_keyboard(lang))
        return

    await message.answer(
        get_text(lang, "select_plant"),
        reply_markup=get_plants_keyboard(plants, lang, show_back_to_categories=True)
    )


@dp.message(lambda message: message.text in ["📚 ALLE SORTEN", "📚 ALL STRAINS", "📚 ВСЕ СОРТА"])
async def show_all_plants(message: Message):
    """Показать все сорта"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    plants = get_plants_for_category(user_id, "all", lang)

    await message.answer(
        get_text(lang, "select_plant"),
        reply_markup=get_plants_keyboard(plants, lang, show_back_to_categories=True)
    )


@dp.message(lambda message: message.text in ["📦 ZUM MANAGER", "📦 CONTACT MANAGER", "📦 К МЕНЕДЖЕРУ"])
async def order(message: Message):
    """Оформление заказа - сразу открывает чат с менеджером"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    manager = MANAGER_USERNAME
    manager_clean = manager.replace("@", "")
    manager_link = f"https://t.me/{manager_clean}"

    if lang == Language.RU:
        text = f"📦 Нажмите на ссылку, чтобы связаться с менеджером:\n👉 {manager_link}\n\nИли напишите напрямую: {manager}"
    elif lang == Language.EN:
        text = f"📦 Click the link to contact the manager:\n👉 {manager_link}\n\nOr write directly: {manager}"
    else:
        text = f"📦 Klicken Sie auf den Link, um den Manager zu kontaktieren:\n👉 {manager_link}\n\nOder schreiben Sie direkt: {manager}"

    await message.answer(text, reply_markup=get_back_to_menu_keyboard(lang))


# ВАЖНО: Обработчик выбора сорта - ДОЛЖЕН БЫТЬ ПОСЛЕ ОСТАЛЬНЫХ ОБРАБОТЧИКОВ
# Создаём список всех названий растений
ALL_PLANT_NAMES = [plant.display_name for plant in get_all_plants()]


@dp.message(lambda message: message.text in ALL_PLANT_NAMES)
async def show_plant_details(message: Message):
    """Показать детальную информацию о растении"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    plant_name = message.text
    print(f"DEBUG: Выбран сорт: {plant_name}, язык: {lang}")

    # Ищем в какой категории находится это растение
    categories = ["all", "sativa", "indica", "hybrid"]
    found_category = None
    found_index = None

    for category in categories:
        plants = get_plants_for_category(user_id, category, lang)
        print(f"DEBUG: Категория {category}, найдено растений: {len(plants)}")
        for idx, p in enumerate(plants):
            print(f"DEBUG: Сравниваем {p.display_name} с {plant_name}")
            if p.display_name == plant_name:
                found_category = category
                found_index = idx
                print(f"DEBUG: Найдено! Категория: {category}, индекс: {idx}")
                break
        if found_category:
            break

    if found_category and found_index is not None:
        await show_plant_by_index(message, user_id, lang, found_category, found_index, is_callback=False)
    else:
        print(f"DEBUG: НЕ НАЙДЕНО! Сорт {plant_name} не найден в категориях")
        await message.answer(get_text(lang, "select_plant"), reply_markup=get_category_keyboard(lang))


# Обработчики навигации
@dp.callback_query(lambda c: c.data.startswith("nav_prev_"))
async def nav_prev(callback: CallbackQuery):
    """Навигация - предыдущее растение"""
    data = callback.data.split("_")
    category = data[2]
    current_index = int(data[3])

    user_id = callback.from_user.id
    lang = get_user_language(user_id)

    new_index = current_index - 1
    await show_plant_by_index(callback, user_id, lang, category, new_index, is_callback=True)


@dp.callback_query(lambda c: c.data.startswith("nav_next_"))
async def nav_next(callback: CallbackQuery):
    """Навигация - следующее растение"""
    data = callback.data.split("_")
    category = data[2]
    current_index = int(data[3])

    user_id = callback.from_user.id
    lang = get_user_language(user_id)

    new_index = current_index + 1
    await show_plant_by_index(callback, user_id, lang, category, new_index, is_callback=True)


@dp.callback_query(lambda c: c.data.startswith("back_to_categories_"))
async def back_to_categories_callback(callback: CallbackQuery):
    """Возврат к категориям из инлайн-клавиатуры"""
    user_id = callback.from_user.id
    lang = get_user_language(user_id)

    await callback.message.delete()
    await callback.message.answer(
        get_text(lang, "select_category"),
        reply_markup=get_category_keyboard(lang)
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "back_to_main_menu")
async def back_to_main_menu_callback(callback: CallbackQuery):
    """Возврат в главное меню"""
    user_id = callback.from_user.id
    lang = get_user_language(user_id)

    # Очищаем кэш для пользователя
    if user_id in category_cache:
        del category_cache[user_id]

    await callback.message.delete()
    await callback.message.answer(
        get_text(lang, "welcome"),
        reply_markup=get_main_menu_keyboard(lang)
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "make_order")
async def make_order_callback(callback: CallbackQuery):
    """Оформление заказа"""
    user_id = callback.from_user.id
    lang = get_user_language(user_id)

    order_text = get_text(lang, "order_info")
    await callback.message.answer(order_text, reply_markup=get_back_to_menu_keyboard(lang))
    await callback.answer()


@dp.callback_query(lambda c: c.data == "empty")
async def empty_callback(callback: CallbackQuery):
    """Пустая кнопка - ничего не делает"""
    await callback.answer()


# Возврат к категориям из обычной клавиатуры
@dp.message(lambda message: message.text in ["↩️ Назад к категориям", "↩️ Back to categories", "↩️ Zurück zu Kategorien"])
async def back_to_categories_reply(message: Message):
    """Вернуться к выбору категорий"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    await message.answer(
        get_text(lang, "select_category"),
        reply_markup=get_category_keyboard(lang)
    )


@dp.message(lambda message: message.text in ["🏠 В главное меню", "🏠 Main menu", "🏠 Hauptmenü"])
async def back_to_main_menu_reply(message: Message):
    """Вернуться в главное меню"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    # Очищаем кэш для пользователя
    if user_id in category_cache:
        del category_cache[user_id]

    welcome_text = get_text(lang, "welcome")
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(lang))


# Смена языка
@dp.message(lambda message: message.text in ["🌐 ENGLISH / РУССКИЙ", "🌐 DEUTSCH / РУССКИЙ", "🌐 DEUTSCH / ENGLISH"])
async def change_language_menu(message: Message):
    """Показать меню смены языка"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    from aiogram.utils.keyboard import ReplyKeyboardBuilder

    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🇩🇪 DEUTSCH"))
    builder.row(KeyboardButton(text="🇬🇧 ENGLISH"))
    builder.row(KeyboardButton(text="🇷🇺 РУССКИЙ"))

    if lang == Language.RU:
        back_text = "↩️ Назад"
    elif lang == Language.EN:
        back_text = "↩️ Back"
    else:
        back_text = "↩️ Zurück"

    builder.row(KeyboardButton(text=back_text))

    keyboard = builder.as_markup(resize_keyboard=True)

    if lang == Language.RU:
        text = "🌐 Выберите язык:"
    elif lang == Language.EN:
        text = "🌐 Select language:"
    else:
        text = "🌐 Wählen Sie eine Sprache:"

    await message.answer(text, reply_markup=keyboard)


@dp.message(lambda message: message.text in ["🇩🇪 DEUTSCH", "🇬🇧 ENGLISH", "🇷🇺 РУССКИЙ"])
async def set_language(message: Message):
    """Установка выбранного языка"""
    user_id = message.from_user.id

    if message.text == "🇩🇪 DEUTSCH":
        user_languages[user_id] = Language.DE
        lang = Language.DE
    elif message.text == "🇬🇧 ENGLISH":
        user_languages[user_id] = Language.EN
        lang = Language.EN
    else:
        user_languages[user_id] = Language.RU
        lang = Language.RU

    # Очищаем кэш при смене языка
    if user_id in category_cache:
        del category_cache[user_id]

    welcome_text = get_text(lang, "welcome")
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(lang))


@dp.message(lambda message: message.text in ["↩️ Назад", "↩️ Back", "↩️ Zurück"])
async def back_from_language(message: Message):
    """Вернуться в меню из выбора языка"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    welcome_text = get_text(lang, "welcome")
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(lang))


@dp.message()
async def unknown_command(message: Message):
    """Неизвестная команда"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    await message.answer(
        get_text(lang, "select_category"),
        reply_markup=get_main_menu_keyboard(lang)
    )


async def main():
    """Запуск бота"""
    print("🤖 Бот для продажи Cannabis запущен!")
    print(f"✅ Поддерживается {len(get_all_plants())} сортов")
    print(f"🌐 Языки: Deutsch, English, Русский")
    print(f"📞 Менеджер: {MANAGER_USERNAME}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())