from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

MAIN_MENU_KB = InlineKeyboardBuilder()
MAIN_MENU_KB.add(
    InlineKeyboardButton(text="🎓 Начать поиск", callback_data="create_plan"),
    InlineKeyboardButton(text="📜 История", callback_data="my_history"),
    InlineKeyboardButton(text="ℹ Помощь", callback_data="help")
)
MAIN_MENU_KB.adjust(2)
MAIN_MENU_KB = MAIN_MENU_KB.as_markup()

LOCATION_KB = InlineKeyboardBuilder()
LOCATION_KB.add(
    InlineKeyboardButton(text="🇷🇺 Россия", callback_data="location:russia"),
    InlineKeyboardButton(text="🌍 Другие страны", callback_data="location:other"),
    InlineKeyboardButton(text="🌐 Без разницы", callback_data="location:any")
)
LOCATION_KB.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
LOCATION_KB.adjust(2)
LOCATION_KB = LOCATION_KB.as_markup()

DIRECTION_KB_BUILDER = InlineKeyboardBuilder()
DIRECTION_KB_BUILDER.add(
    InlineKeyboardButton(text="💻 IT/Программирование", callback_data="direction:it"),
    InlineKeyboardButton(text="📈 Экономика", callback_data="direction:econ"),
    InlineKeyboardButton(text="🩺 Медицина", callback_data="direction:med")
)
DIRECTION_KB_BUILDER.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
DIRECTION_KB_BUILDER.adjust(2)
DIRECTION_KB = DIRECTION_KB_BUILDER.as_markup()