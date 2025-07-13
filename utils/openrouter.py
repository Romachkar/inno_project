import os
import httpx
import logging

logger = logging.getLogger(__name__)
async def generate_universities(data):
    prompt = f"""
    🎓 Рассчитай варианты вузов для поступления:
    🏙 Города: {', '.join(data['cities'])}
    🧭 Направление: {data['direction']}
    📊 Баллы ЕГЭ: {', '.join(map(str, data['scores']))}

    🔍 Покажи вузы, где можно поступить с такими баллами в этих городах, но без таблиц, а так же на русском
    """

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"},
                json={
                    "model": "",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 10000000
                },
                timeout=30
            )

            if response.status_code != 200:
                logger.error(f"Ошибка API: {response.text}")
                return "⚠ Сервис временно недоступен"

            response_data = response.json()
            if "choices" not in response_data:
                logger.error(f"Неверный формат ответа: {response_data}")
                return "⚠ Не удалось получить рекомендации"

            raw_response = response_data["choices"][0]["message"]["content"]
            formatted_response = raw_response.replace("1.", "📌").replace("2.", "📌").replace("3.", "📌")
            return formatted_response

        except Exception as e:
            logger.error(f"Ошибка генерации: {str(e)}")
            return "⚠ Сервис временно недоступен"