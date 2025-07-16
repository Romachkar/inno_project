from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.inline import MAIN_MENU_KB
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards.inline import DIRECTION_KB, LOCATION_KB, BACK_KB
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

@router.callback_query(F.data == "create_plan")
async def create_plan(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UniversityForm.location_choice)
    await callback.message.edit_text("🌍 Где вы хотели бы учиться?", reply_markup=LOCATION_KB)


@router.callback_query(F.data.startswith("location:"))
async def handle_location(callback: CallbackQuery, state: FSMContext):
    location_type = callback.data.split(":")[1]
    await state.update_data(location_type=location_type)

    if location_type == "russia":
        await callback.message.edit_text("🏙 Введите город в России:")
        await state.set_state(UniversityForm.cities_russia)

    elif location_type == "other":
        await callback.message.edit_text("🌍 Введите страну и город через запятую (или только страну):")
        await state.set_state(UniversityForm.cities_other)

    else:
        await callback.message.edit_text("🏙 Введите города через запятую:")
        await state.set_state(UniversityForm.cities_other)


@router.message(UniversityForm.cities_russia)
async def process_city_russia(message: Message, state: FSMContext):
    city = message.text.strip()
    await state.update_data(cities=[city])
    await message.answer("✍️ Введите ваши индивидуальные достижения (например: олимпиады, проекты, волонтерство):")
    await state.set_state(UniversityForm.achievements)


@router.message(UniversityForm.cities_other)
async def process_location_other(message: Message, state: FSMContext):
    locations = [loc.strip() for loc in message.text.split(",") if loc.strip()]
    if len(locations) < 1 or len(locations) > 5:
        await message.answer("⚠ Введите от 1 до 5 локаций")
        return

    await state.update_data(cities=locations)
    await message.answer("🧭 Выберите направление:", reply_markup=DIRECTION_KB)



@router.message(UniversityForm.achievements)
async def process_achievements(message: Message, state: FSMContext):
    achievements = message.text.strip()
    if not achievements:
        await message.answer("❌ Пожалуйста, введите достижения")
        return

    await state.update_data(achievements=achievements)
    await state.set_state(UniversityForm.direction)
    await message.answer("🧭 Выберите направление:", reply_markup=DIRECTION_KB)


@router.callback_query(F.data.startswith("direction:"))
async def process_direction(callback: CallbackQuery, state: FSMContext):
    direction = callback.data.split(":")[1]
    await state.update_data(direction=direction)

    if callback.message.text != "✍️ Введите баллы ЕГЭ в формате:\nПример:\nПроф. мат 100\nРусский язык 100\nИнформатика 100":
        await callback.message.edit_text(
            "✍️ Введите баллы ЕГЭ в формате:\n"
            "Пример:\n"
            "Проф. мат 100\n"
            "Русский язык 100\n"
            "Информатика 100"
        )

    await state.set_state(UniversityForm.scores)


@router.message(UniversityForm.scores)
async def process_scores(message: Message, state: FSMContext):
    lines = [line.strip() for line in message.text.split("\n") if line.strip()]
    scores = {}

    for line in lines:
        match = re.match(r"^(.+?)\s+(\d+)$", line)
        if not match:
            await message.answer(
                "❌ Неверный формат. Используйте:\nПример:\nПроф. мат 100\nРусский язык 100\nИнформатика 100")
            return

        subject = match.group(1).strip()
        score = int(match.group(2))

        if not (0 <= score <= 100):
            await message.answer("❌ Баллы должны быть от 0 до 100")
            return

        scores[subject] = score

    data = await state.get_data()
    data["scores"] = scores
    await state.clear()

    await message.answer("🕒 Генерируем рекомендации...")
    recommendations = await generate_universities(data)
    recommendations = re.sub(r"^(.#)\s+(\d+)$", recommendations)
    await message.answer("🎓 Подходящие вузы:")
    await message.answer(recommendations, parse_mode='Markdown')
    await message.answer("🔍 Начать поиск снова?", reply_markup=MAIN_MENU_KB)