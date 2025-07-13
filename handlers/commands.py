from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from states.university import UserStates

router = Router()

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await message.answer(
        "Привет! Я помогу подобрать тебе вуз по твоим баллам за экзамен и предпочтениям. Сначала введите города через запятую (например: Москва, Санкт-Петербург)"
    )
    await state.set_state(UserStates.cities)