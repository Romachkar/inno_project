
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.inline import MAIN_MENU_KB

router = Router()


def get_user_name(event: Message | CallbackQuery):
    if isinstance(event, Message):
        user = event.from_user
    else:
        user = event.from_user

    if user.full_name:
        return user.full_name
    elif user.username:
        return f"@{user.username}"
    else:
        return "Пользователь"

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    user_name = get_user_name(message)

    await state.clear()
    await message.answer(
        f"🎓 Привет, {user_name}! Я помогу выбрать вуз по твоим результатам ЕГЭ и достижениям. Начнём!",
        reply_markup=MAIN_MENU_KB
    )