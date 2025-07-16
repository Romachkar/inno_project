from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.inline import MAIN_MENU_KB
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards.inline import DIRECTION_KB, LOCATION_KB, ACHIEVEMENTS_KB, BACK_KB
from states.university import UniversityForm
import logging
from utils.database import db
from utils.openrouter import generate_universities
import re
logger = logging.getLogger(__name__)
router = Router()



@router.callback_query(F.data == "main_menu")
@router.message(CommandStart())
async def main_menu(event: Message | CallbackQuery, state: FSMContext):
    await state.clear()

    if isinstance(event, CallbackQuery):
        await event.message.edit_text("Добро пожаловать! Выберите действие:", reply_markup=MAIN_MENU_KB)
    else:
        await event.answer("Добро пожаловать! Выберите действие:", reply_markup=MAIN_MENU_KB)

@router.callback_query(F.data == "my_history")
async def show_history(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    history = db.get_user_plans(user_id)

    if not history:
        await callback.message.edit_text("📜 У вас ещё нет истории запросов", reply_markup=BACK_KB)
        return

    kb = InlineKeyboardBuilder()
    for entry in history:
        kb.button(text=f"{entry['query_text']} ({entry['timestamp']})", callback_data=f"view_plan_{entry['id']}")
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    kb.adjust(1)

    await callback.message.edit_text("📜 Ваши запросы:")
    await callback.message.edit_reply_markup(reply_markup=kb.as_markup())
    kb = InlineKeyboardBuilder()
    for entry in history:
        kb.button(text=f"{entry['query_text']} ({entry['timestamp']})", callback_data=f"view_plan_{entry['id']}")
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    kb.adjust(1)

    await callback.message.edit_text("📜 Ваши запросы:")
    await callback.message.edit_reply_markup(reply_markup=kb.as_markup())


@router.callback_query(F.data == "help")
async def help_command(callback: CallbackQuery, state: FSMContext):
    help_text = (
        "📚 **Как со мной работать**:\n\n"
        "1. Нажмите **«Создать план»** и выберите страну\n"
        "2. Введите город или страну\n"
        "3. Выберите направление\n"
        "4. Введите баллы ЕГЭ в формате:\n"
        "Пример:\n"
        "Проф. мат 100\n"
        "Русский язык 100\n"
        "Информатика 100"
    )

    if callback.message.text != help_text:
        await callback.message.edit_text(help_text, reply_markup=BACK_KB)


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if callback.message.text != "🎓 Добро пожаловать! Выберите действие:":
        await callback.message.edit_text("🎓 Добро пожаловать! Выберите действие:", reply_markup=MAIN_MENU_KB)