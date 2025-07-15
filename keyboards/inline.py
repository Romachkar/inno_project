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

LOCATION_KB_BUILDER = InlineKeyboardBuilder()
LOCATION_KB_BUILDER.add(
    InlineKeyboardButton(text="🇷🇺 Россия", callback_data="location:russia"),
    InlineKeyboardButton(text="🌍 Другие страны", callback_data="location:other"),
    InlineKeyboardButton(text="🌐 Без разницы", callback_data="location:any")
)
LOCATION_KB_BUILDER.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
LOCATION_KB_BUILDER.adjust(2)
LOCATION_KB = LOCATION_KB_BUILDER.as_markup()

ACHIEVEMENTS_KB_BUILDER = InlineKeyboardBuilder()
ACHIEVEMENTS_KB_BUILDER.add(
    InlineKeyboardButton(text="🏅 Олимпиады", callback_data="achievement:olympic"),
    InlineKeyboardButton(text="📚 Портфолио", callback_data="achievement:portfolio"),
    InlineKeyboardButton(text="🌍 Волонтерство", callback_data="achievement:volunteer"),
    InlineKeyboardButton(text="Научные проекты", callback_data="achievement:projects"),
    InlineKeyboardButton(text="🏅 Золотая медаль", callback_data="achievement:zoloto")
)
ACHIEVEMENTS_KB_BUILDER.add(InlineKeyboardButton(text="✅ Подтвердить", callback_data="achievements_done"))
ACHIEVEMENTS_KB_BUILDER.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
ACHIEVEMENTS_KB_BUILDER.adjust(2)

ACHIEVEMENTS_KB = ACHIEVEMENTS_KB_BUILDER.as_markup()
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