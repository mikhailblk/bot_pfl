from config import MANAGER_USERNAME
from enum import Enum

class Language(Enum):
    DE = "deutsch"
    EN = "english"
    RU = "russian"


# Все тексты на трёх языках
TEXTS = {
    Language.DE: {
        "welcome": "🌿 Willkommen in unserem Cannabis-Shop! 🌿\n\nWir bieten eine große Auswahl an hochwertigen Sorten für Sie.",
        "catalog": "📚 KATALOG",
        "order": "📦 BESTELLEN",
        "change_language": "🌐 ENGLISH / РУССКИЙ",
        "select_category": "📂 Wählen Sie eine Kategorie:",
        "sativa": "🌿 SATIVA",
        "indica": "🌸 INDICA",
        "hybrid": "🔀 HYBRID",
        "all": "📚 ALLE SORTEN",
        "select_plant": "🌿 Wählen Sie eine Sorte:",
        "order_button": "📦 ZUM MANAGER",  # Новая кнопка
        "order_info": f"📦 Kontaktieren Sie unseren Manager direkt: {MANAGER_USERNAME}",
        "language_changed": "Sprache wurde geändert auf: Deutsch",
        "back_to_menu": "↩️ Zurück zum Menü",
        "back_to_categories": "↩️ Zurück zu Kategorien",
        "no_plants": "🌿 In dieser Kategorie gibt es noch keine Sorten",
    },
    Language.EN: {
        "welcome": "🌿 Welcome to our Cannabis Shop! 🌿\n\nWe offer a wide selection of high-quality strains for you.",
        "catalog": "📚 CATALOG",
        "order": "📦 ORDER",
        "change_language": "🌐 DEUTSCH / РУССКИЙ",
        "select_category": "📂 Select a category:",
        "sativa": "🌿 SATIVA",
        "indica": "🌸 INDICA",
        "hybrid": "🔀 HYBRID",
        "all": "📚 ALL STRAINS",
        "select_plant": "🌿 Select a strain:",
        "order_button": "📦 CONTACT MANAGER",  # Новая кнопка
        "order_info": f"📦 Contact our manager directly: {MANAGER_USERNAME}",
        "language_changed": "Language changed to: English",
        "back_to_menu": "↩️ Back to Menu",
        "back_to_categories": "↩️ Back to Categories",
        "no_plants": "🌿 No strains in this category yet",
    },
    Language.RU: {
        "welcome": "🌿 Добро пожаловать в наш Cannabis-магазин! 🌿\n\nМы предлагаем широкий выбор качественных сортов.",
        "catalog": "📚 КАТАЛОГ",
        "order": "📦 ЗАКАЗАТЬ",
        "change_language": "🌐 DEUTSCH / ENGLISH",
        "select_category": "📂 Выберите категорию:",
        "sativa": "🌿 САТИВА",
        "indica": "🌸 ИНДИКА",
        "hybrid": "🔀 ГИБРИД",
        "all": "📚 ВСЕ СОРТА",
        "select_plant": "🌿 Выберите сорт:",
        "order_button": "📦 К МЕНЕДЖЕРУ",  # Новая кнопка
        "order_info": f"📦 Свяжитесь с нашим менеджером напрямую: {MANAGER_USERNAME}",
        "language_changed": "Язык изменён на: Русский",
        "back_to_menu": "↩️ Вернуться в меню",
        "back_to_categories": "↩️ Назад к категориям",
        "no_plants": "🌿 В этой категории пока нет сортов",
    }
}

def get_text(lang: Language, key: str) -> str:
    """Получить текст на нужном языке"""
    return TEXTS.get(lang, TEXTS[Language.DE]).get(key, key)