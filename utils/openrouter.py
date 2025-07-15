import os
import httpx
import logging

logger = logging.getLogger(__name__)


async def generate_universities(data):
    prompt = f"""
Ты — квалифицированный помощник в выборе вузов для поступления. Учитывая предоставленные данные, ты должен подобрать наиболее подходящие варианты вузов, где абитуриент имеет высокие шансы на зачисление. 
Дополнительные параметры: бюджетное место / платное, форма обучения (очная / заочная), престиж вуза, наличие общежития, военная кафедра, международные программы и т.д.
На основе этих данных предложи ТОП-4 вузов, которые:

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

    prompt += f"Направление: {data['direction']}\n"
    scores_text = "\n".join(f"- {subj}: {score}" for subj, score in data["scores"].items())
    prompt += f"Баллы ЕГЭ:\n{scores_text}\n"
    prompt += """ПИШИ ТОЛЬКО НА РУССКОМ, КРАСИВОЕ ФОРМАТИРОВАНИЕ ТЕКСТА, подробно про каждый университет, так же примерно переведи баллы егэ в систему оценивания знаний в той стране в которую хочет поступить пользователь"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions ",
                headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"},
                json={
                    "model": "tngtech/deepseek-r1t2-chimera:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000
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