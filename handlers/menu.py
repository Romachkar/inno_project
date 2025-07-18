from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
import sqlite3
from utils.database import db
import re
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards.inline import MAIN_MENU_KB, DIRECTION_KB, LOCATION_KB, BACK_KB
from states.university import UniversityForm
from utils.openrouter import generate_universities
logger = logging.getLogger(__name__)
router = Router()

def get_user_name(event: Message | CallbackQuery) -> str:
    user = event.from_user
    return user.full_name or f"@{user.username}" or "Пользователь"


@router.callback_query(F.data == "main_menu")
@router.message(CommandStart())
async def main_menu(event: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    user_name = get_user_name(event)
    text = f"👋 Привет, {user_name}! Выбери действие:"

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=MAIN_MENU_KB)
    else:
        await event.answer(text, reply_markup=MAIN_MENU_KB)


@router.callback_query(F.data == "my_history")
async def show_history(callback: CallbackQuery):
    user_id = callback.from_user.id
    history = db.get_user_plans(user_id)

    if not history:
        await callback.message.edit_text("📜 У вас ещё нет истории запросов", reply_markup=BACK_KB)
        return

    kb = InlineKeyboardBuilder()
    for entry in history:
        timestamp = entry['timestamp'].split()[0] if entry['timestamp'] else "N/A"
        kb.add(InlineKeyboardButton(
            text=f"{entry['query_text']} ({timestamp})",
            callback_data=f"view_plan_{entry['id']}"
        ))
    kb.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    kb.adjust(1)

    await callback.message.edit_text("📜 Ваши запросы:", reply_markup=kb.as_markup())


@router.callback_query(F.data == "clear_history")
async def clear_history(callback: CallbackQuery):
    user_id = callback.from_user.id
    try:
        db.conn.execute('DELETE FROM queries WHERE user_id = ?', (user_id,))
        db.conn.commit()
        await callback.message.edit_text("✅ История запросов очищена", reply_markup=BACK_KB)
    except sqlite3.Error as e:
        logger.error(f"Ошибка очистки истории: {str(e)}")
        await callback.message.edit_text("❌ Не удалось очистить историю", reply_markup=BACK_KB)


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
        await callback.message.edit_text("🌐 Введите города через запятую:")
        await state.set_state(UniversityForm.cities_other)


@router.message(UniversityForm.cities_russia)
async def process_city_russia(message: Message, state: FSMContext):
    city = message.text.strip()
    await state.update_data(cities=[city])
    await message.answer("🧭 Выберите направление:", reply_markup=DIRECTION_KB)
    await state.set_state(UniversityForm.direction)


@router.message(UniversityForm.cities_other)
async def process_location_other(message: Message, state: FSMContext):
    locations = [loc.strip() for loc in message.text.split(",") if loc.strip()]
    if len(locations) < 1 or len(locations) > 5:
        await message.answer("⚠ Введите от 1 до 5 локаций")
        return

    await state.update_data(cities=locations)
    await message.answer("🧭 Выберите направление:", reply_markup=DIRECTION_KB)
    await state.set_state(UniversityForm.direction)


@router.callback_query(F.data.startswith("direction:"))
async def process_direction(callback: CallbackQuery, state: FSMContext):
    direction = callback.data.split(":")[1]
    await state.update_data(direction=direction)
    user_name = get_user_name(callback)

    await callback.message.edit_text(
        f"✍️ {user_name}, введите баллы ЕГЭ в формате:\n"
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
                "❌ Неверный формат. Используйте:\n"
                "Пример:\n"
                "Проф. мат 100\n"
                "Русский язык 100\n"
                "Информатика 100"
            )
            return

        subject = match.group(1).strip()
        score = int(match.group(2))

        if not (0 <= score <= 100):
            await message.answer("❌ Баллы должны быть от 0 до 100")
            return

        scores[subject] = score

    await state.update_data(scores=scores)
    await message.answer("🏆 Введите ваши индивидуальные достижения (олимпиады, проекты, волонтерство и т.д.):")
    await state.set_state(UniversityForm.achievements)


@router.message(UniversityForm.achievements)
async def process_achievements(message: Message, state: FSMContext):
    achievements = message.text.strip()
    if not achievements:
        await message.answer("❌ Пожалуйста, введите ваши достижения")
        return

    data = await state.get_data()
    data["achievements"] = achievements

    direction = data.get('direction', 'не указано')
    cities = data.get('cities', [])
    cities_str = ', '.join(cities) if cities else 'не указаны'
    scores_str = ', '.join([f"{subj} {score}" for subj, score in data.get('scores', {}).items()])
    achievements_short = (achievements[:20] + '...') if len(achievements) > 20 else achievements

    query_text = f"{direction} | {cities_str} | {scores_str} | Достижения: {achievements_short}"

    await message.answer("🕒 Ищем вузы для вас...")
    recommendations = await generate_universities(data)

    db.log_query(message.from_user.id, query_text, recommendations)
    recommendations = re.sub(r'#\w+', '', recommendations)
    await message.answer("🎓 Подходящие вузы:")
    await message.answer(recommendations, parse_mode="Markdown", reply_markup=MAIN_MENU_KB)

    await state.clear()
