from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards.inline import directions
from states.university import UserStates
from utils.openrouter import generate_universities
import logging
import re
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
    lines = [line.strip() for line in message.text.split("\n") if line.strip()]
    scores = {}

    for line in lines:
        match = re.match(r'^(.+?)\s+(\d+)$', line)
        if not match:
            await message.answer(f"❌ Ошибка в строке: {line}")
            return
        subject = match.group(1).strip()
        score = int(match.group(2))
        scores[subject] = score

    data = await state.get_data()
    data["scores"] = scores
    await state.clear()

    recommendations = await generate_universities(data)
    if not isinstance(recommendations, str):
        recommendations = "⚠ Не удалось получить рекомендации"

    await message.answer("🎓 Подходящие вузы:")
    await message.answer(recommendations)