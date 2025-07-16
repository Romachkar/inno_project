from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


MAIN_MENU_KB_BUILDER = InlineKeyboardBuilder()
MAIN_MENU_KB_BUILDER.add(
    InlineKeyboardButton(text="🎓 Старт", callback_data="create_plan"),
    InlineKeyboardButton(text="📜 История", callback_data="my_history"),
    InlineKeyboardButton(text="ℹ Помощь", callback_data="help")
)
MAIN_MENU_KB_BUILDER.adjust(2)
MAIN_MENU_KB = MAIN_MENU_KB_BUILDER.as_markup()

lang_kb_builder = InlineKeyboardBuilder()
lang_kb_builder.add(
    InlineKeyboardButton(text="Русский язык", callback_data="lang:russia"),
    InlineKeyboardButton(text="English language", callback_data="lang:eng"),
    InlineKeyboardButton(text="Беларуская мова", callback_data="lang:bel")
)
lang_kb_builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
lang_kb_builder.adjust(2)
lang_kb = lang_kb_builder.as_markup()

LOCATION_KB_BUILDER = InlineKeyboardBuilder()
LOCATION_KB_BUILDER.add(
    InlineKeyboardButton(text="🇷🇺 Россия", callback_data="location:russia"),
    InlineKeyboardButton(text="🌍 Другие страны", callback_data="location:other"),
    InlineKeyboardButton(text="🌐 Без разницы", callback_data="location:any")
)
LOCATION_KB_BUILDER.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
LOCATION_KB_BUILDER.adjust(2)
LOCATION_KB = LOCATION_KB_BUILDER.as_markup()


DIRECTION_KB_BUILDER = InlineKeyboardBuilder()
DIRECTION_KB_BUILDER.add(
    InlineKeyboardButton(text="💻 IT/Программирование", callback_data="direction:it"),
    InlineKeyboardButton(text="📈 Экономика", callback_data="direction:econ"),
    InlineKeyboardButton(text="🩺 Медицина", callback_data="direction:med")
)
DIRECTION_KB_BUILDER.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
DIRECTION_KB_BUILDER.adjust(2)
DIRECTION_KB = DIRECTION_KB_BUILDER.as_markup()

BACK_KB_BUILDER = InlineKeyboardBuilder()
BACK_KB_BUILDER.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
BACK_KB = BACK_KB_BUILDER.as_markup()