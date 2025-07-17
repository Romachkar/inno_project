from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.inline import MAIN_MENU_KB

router = Router()

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🎓 Добро пожаловать! Выберите действие:", reply_markup=MAIN_MENU_KB)