from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards.inline import directions
from states.university import UserStates
from utils.openrouter import generate_universities
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.message(UserStates.cities)
async def process_cities(message: Message, state: FSMContext):
    cities = [city.strip() for city in message.text.split(",")]

    if len(cities) < 1 or len(cities) > 5:
        await message.answer("⚠ Введите от 1 до 5 городов через запятую (например: Москва, Санкт-Петербург)")
        return

    await state.update_data(cities=cities)
    await message.answer("✅ Города сохранены!", parse_mode="Markdown")
    await message.answer("🎓 Выберите направление:", reply_markup=directions)



@router.callback_query(lambda c: c.data.startswith("direction:"))
async def process_direction(callback: CallbackQuery, state: FSMContext):
    direction = callback.data.split(":")[1]
    direction_emoji = {
        "it": "💻",
        "econ": "📈",
        "med": "🩺"
    }.get(direction, "❓")

    await state.update_data(direction=direction)

    if callback.message.text != f"{direction_emoji} Введите свои баллы егэ и предметы в таком формате \n (Проф. мат 100 \n Русский язык 100\n Информатика 100)":
        await callback.message.edit_text(f"{direction_emoji} Введите свои баллы егэ и предметы в таком формате \n (Проф. мат 100 \n Русский язык 100\n Информатика 100)")

    await state.set_state(UserStates.score)


@router.message(UserStates.score)
async def process_scores(message: Message, state: FSMContext):
    try:
        score = list(map(int, message.text.split()))
        if any(score < 0 or score > 100 for score in score):
            raise ValueError
    except:
        await message.answer("❌ Неверный формат баллов. Введите числа от 0 до 100 через пробел")
        return

    data = await state.get_data()
    data["scores"] = score

    recommendations = await generate_universities(data)

    await message.answer("🎓 Подходящие вузы:")
    await message.answer(recommendations)
    await state.clear()