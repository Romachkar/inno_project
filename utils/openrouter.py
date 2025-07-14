import os
import httpx
import logging

logger = logging.getLogger(__name__)


async def generate_universities(data):
    prompt = f"""
    Рассчитай подходящие вузы:
    Города: {', '.join(data['cities'])}
    Направление: {data['direction']}
    Баллы ЕГЭ:
    """
    for subject, score in data["scores"].items():
        prompt += f"  - {subject}: {score}\n"

    prompt += "Не используй звездочки, подчеркивания и другие символы разметки. Пиши чистый текст."

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"},
                json={
                    "model": "deepseek/deepseek-r1:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2000
                },
                timeout=30
            )

            logger.info(f"API Response: {response.status_code}, {response.text}")

            if response.status_code != 200:
                logger.error(f"Ошибка API: {response.text}")
                return "⚠ Сервис временно недоступен"

            response_data = response.json()

            if "choices" not in response_data or not response_data["choices"]:
                logger.error(f"Неверный формат ответа: {response_data}")
                return "⚠ Не удалось получить рекомендации"
            plan = response_data["choices"][0]["message"]["content"]

            if not isinstance(plan, str):
                logger.error("Неверный тип ответа от нейросети")
                return "⚠ Неверный формат ответа от нейросети"

            return plan

        except Exception as e:
            logger.error(f"Ошибка генерации: {str(e)}")
            return "⚠ Не удалось получить рекомендации"