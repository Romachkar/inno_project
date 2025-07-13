from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

directions = InlineKeyboardBuilder()
directions.add(
    InlineKeyboardButton(text="💻 IT/Программирование", callback_data="direction:it"),
    InlineKeyboardButton(text="📈 Экономика", callback_data="direction:econ"),
    InlineKeyboardButton(text="🩺 Медицина", callback_data="direction:med")
)
directions.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
directions.adjust(2)
directions = directions.as_markup()