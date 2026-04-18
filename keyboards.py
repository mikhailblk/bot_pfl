from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from language import Language, get_text
from plants_data import get_all_plants, get_plants_by_genetics_type


def get_main_menu_keyboard(lang: Language) -> ReplyKeyboardMarkup:
    """Главное меню с большой кнопкой каталога"""

    catalog_button = KeyboardButton(text=get_text(lang, "catalog"))
    order_button = KeyboardButton(text=get_text(lang, "order_button"))  # Изменено

    if lang == Language.DE:
        lang_button_text = "🌐 ENGLISH / РУССКИЙ"
    elif lang == Language.EN:
        lang_button_text = "🌐 DEUTSCH / РУССКИЙ"
    else:
        lang_button_text = "🌐 DEUTSCH / ENGLISH"

    lang_button = KeyboardButton(text=lang_button_text)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [catalog_button],
            [order_button, lang_button]
        ],
        resize_keyboard=True
    )

    return keyboard


def get_category_keyboard(lang: Language) -> ReplyKeyboardMarkup:
    """Клавиатура выбора категории"""

    sativa_text = get_text(lang, "sativa")
    indica_text = get_text(lang, "indica")
    hybrid_text = get_text(lang, "hybrid")
    all_text = get_text(lang, "all")

    if lang == Language.RU:
        back_text = "🏠 В главное меню"
    elif lang == Language.EN:
        back_text = "🏠 Main menu"
    else:
        back_text = "🏠 Hauptmenü"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=sativa_text)],
            [KeyboardButton(text=indica_text)],
            [KeyboardButton(text=hybrid_text)],
            [KeyboardButton(text=all_text)],
            [KeyboardButton(text=back_text)]
        ],
        resize_keyboard=True
    )

    return keyboard


def get_plants_keyboard(plants, lang: Language, show_back_to_categories: bool = True) -> ReplyKeyboardMarkup:
    """Клавиатура со списком растений"""

    plant_buttons = []
    for plant in plants:
        plant_buttons.append([KeyboardButton(text=plant.display_name)])

    if show_back_to_categories:
        if lang == Language.RU:
            back_text = "↩️ Назад к категориям"
        elif lang == Language.EN:
            back_text = "↩️ Back to categories"
        else:
            back_text = "↩️ Zurück zu Kategorien"

        plant_buttons.append([KeyboardButton(text=back_text)])

    keyboard = ReplyKeyboardMarkup(
        keyboard=plant_buttons,
        resize_keyboard=True
    )

    return keyboard


def get_plant_navigation_keyboard(lang: Language, current_index: int, total: int, category: str, plant_id: str) -> InlineKeyboardMarkup:
    """Инлайн-клавиатура для навигации между растениями"""

    builder = InlineKeyboardBuilder()

    # Первый ряд: ◀️ Назад | Текущий номер | Вперед ▶️
    if current_index > 0:
        builder.add(InlineKeyboardButton(
            text=f"◀️ {current_index}",
            callback_data=f"nav_prev_{category}_{current_index}_{plant_id}"
        ))
    else:
        builder.add(InlineKeyboardButton(text="◀️ --", callback_data="empty"))

    builder.add(InlineKeyboardButton(
        text=f"{current_index + 1} / {total}",
        callback_data="empty"
    ))

    if current_index < total - 1:
        builder.add(InlineKeyboardButton(
            text=f"{current_index + 2} ▶️",
            callback_data=f"nav_next_{category}_{current_index}_{plant_id}"
        ))
    else:
        builder.add(InlineKeyboardButton(text="-- ▶️", callback_data="empty"))

    builder.adjust(3)

    # Второй ряд: Назад к категориям | В главное меню
    if lang == Language.RU:
        back_text = "↩️ Назад к категориям"
        menu_text = "🏠 В главное меню"
    elif lang == Language.EN:
        back_text = "↩️ Back to categories"
        menu_text = "🏠 Main menu"
    else:
        back_text = "↩️ Zurück zu Kategorien"
        menu_text = "🏠 Hauptmenü"

    builder.row(
        InlineKeyboardButton(text=back_text, callback_data=f"back_to_categories_{category}"),
        InlineKeyboardButton(text=menu_text, callback_data="back_to_main_menu")
    )

    # Третий ряд: Сделать заказ - теперь сразу к менеджеру
    if lang == Language.RU:
        order_text = "📦 СВЯЗАТЬСЯ С МЕНЕДЖЕРОМ"
    elif lang == Language.EN:
        order_text = "📦 CONTACT MANAGER"
    else:
        order_text = "📦 MANAGER KONTAKTIEREN"

    builder.row(InlineKeyboardButton(text=order_text, callback_data="contact_manager"))

    return builder.as_markup()


def get_back_to_categories_keyboard(lang: Language) -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой возврата к категориям"""

    if lang == Language.RU:
        back_text = "↩️ Назад к категориям"
        menu_text = "🏠 В главное меню"
    elif lang == Language.EN:
        back_text = "↩️ Back to categories"
        menu_text = "🏠 Main menu"
    else:
        back_text = "↩️ Zurück zu Kategorien"
        menu_text = "🏠 Hauptmenü"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=back_text)],
            [KeyboardButton(text=menu_text)]
        ],
        resize_keyboard=True
    )

    return keyboard


def get_back_to_menu_keyboard(lang: Language) -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой возврата в меню"""

    if lang == Language.RU:
        menu_text = "🏠 В главное меню"
    elif lang == Language.EN:
        menu_text = "🏠 Main menu"
    else:
        menu_text = "🏠 Hauptmenü"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=menu_text)]
        ],
        resize_keyboard=True
    )

    return keyboard