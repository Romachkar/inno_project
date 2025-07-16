import os
import httpx
import logging

logger = logging.getLogger(__name__)


async def generate_universities(data):
    prompt = f"""
Ты — квалифицированный помощник в выборе вузов для поступления. Учитывая предоставленные данные, ты должен подобрать наиболее подходящие варианты вузов, где абитуриент имеет высокие шансы на зачисление. 
Дополнительные параметры: бюджетное место / платное, форма обучения (очная / заочная), престиж вуза, наличие общежития, военная кафедра, международные программы и т.д.
На основе этих данных предложи ТОП-10, если задан 5 городов, если задано 4 города 8 вузов, если 3 то 6, а если 2 то 5 и на 1 город 5 в  узов, которые:

Соответствуют уровню ЕГЭ.
Расположены в желаемых регионах.
Имеют сильную подготовку по выбранному направлению.
Учитывают дополнительные предпочтения.
Для каждого вуза укажи:

Название и краткое описание (престиж, специализация).
Проходной балл по направлению за последние годы (если известно).
Преимущества обучения именно в этом вузе.
Ссылку на официальный сайт или направление.
    """

    if data.get("location_type") == "russia":
        prompt += f"Города (Россия): {', '.join(data['cities'])}\n"
    elif data.get("location_type") == "other":
        prompt += f"Страны/города: {', '.join(data['cities'])}\n"
    else:
        prompt += f"Города: {', '.join(data['cities'])}\n"

    if "achievements" in data:
        prompt += f"🏆 Индивидуальные достижения: {data['achievements']}\n"

    if "achievements" in data:
        achievements_text = ", ".join({
        "olympic": "Олимпиады",
        "portfolio": "Портфолио",
        "volunteer": "Волонтерство",
        "projects": "Научные проекты"
        }.get(a, a) for a in data["achievements"])
        prompt += f"🏆 Индивидуальные достижения: {achievements_text}\n"

    prompt += f"Направление: {data['direction']}\n"
    scores_text = "\n".join(f"- {subj}: {score}" for subj, score in data["scores"].items())
    prompt += f"Баллы ЕГЭ:\n{scores_text}\n"
    prompt += """ПИШИ ТОЛЬКО НА РУССКОМ, КРАСИВОЕ ФОРМАТИРОВАНИЕ ТЕКСТА, подробно про каждый университет, больше важной информации для пользователя, меньше воды """
    prompt += "ПИШИ ТЕКСТ БЕЗ ИСПОЛЬЗОВАНИЯ '###'"
    prompt += "ПИШИ ТЕКСТ БЫСТРО, так же учитывай какие предметы пользователь сдавал, если он сдавал предметы не подходящие по его направление"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"},
                json={
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 4000
                },
                timeout=30
            )

            if response.status_code != 200:
                logger.error(f"Ошибка API: {response.text}")
                return "⚠ Сервис временно недоступен"

            return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"Ошибка генерации: {str(e)}")
            return "⚠ Не удалось получить рекомендации"