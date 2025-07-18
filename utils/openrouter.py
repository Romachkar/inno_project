import os
import httpx
import logging

logger = logging.getLogger(__name__)


async def generate_universities(data):
    prompt = f"""
Ты — эксперт по высшему образованию, помогающий абитуриентам выбрать оптимальные вузы для поступления. 
Проанализируй следующие данные абитуриента и предложи лучшие варианты вузов:

### Основная информация:
1. **Желаемое место обучения**: 
   - {'Города России: ' + ', '.join(data['cities']) if data.get("location_type") == "russia" else
    'Международные локации: ' + ', '.join(data['cities']) if data.get("location_type") == "other" else
    'Локации: ' + ', '.join(data['cities'])}

2. **Направление подготовки**: {data['direction']}

3. **Баллы ЕГЭ**:
{chr(10).join(f"   - {subject}: {score}" for subject, score in data["scores"].items())}

4. **Индивидуальные достижения**: {data.get('achievements', 'не указаны')}

1. ИСПОЛЬЗУЙ ТОЛЬКО ЭТИ ТЕГИ:
   - **Жирный текст** для заголовков
   - `Моноширинный` для кодов/названий
   - [Ссылки](https://example.com) в квадратных скобках
   
2. ЗАПРЕЩЕНО:
   - Тройные ### и более заголовки
   - HTML-теги
   - Подчеркивания _для курсива_
   - Специальные символы без экранирования: _*[]()~`>#+-=|{}.!

3. ДЛЯ ССЫЛОК:
   - Всегда проверяй закрывающие скобки
   - Используй только абсолютные URL
   - Экранные символы в URL: \\( \\) \\[ \\]

Пример корректной ссылки:
[Сайт МГУ](https://www\.msu\.ru/поступление/программа_123)

4. ДЛЯ СПИСКОВ:
   - Используй дефисы вместо цифр
   - Отступы: 2 пробела для вложенных

Пример:
- Факультет:
  - Направление 1
  - Направление 2

5. ЕСЛИ ТЕКСТ ПРЕВЫШАЕТ 4000 СИМВОЛОВ:
   - Сократи описания
   - Удали менее важные вузы
   - Оставь только ключевую информацию
"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"},
                json={
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 4000,
                    "temperature": 0.3
                },
                timeout=45
            )

            if response.status_code != 200:
                logger.error(f"Ошибка API: {response.status_code} - {response.text}")
                return "⚠️ Сервис временно недоступен. Попробуйте позже."

            result = response.json()["choices"][0]["message"]["content"]

            if "проходной балл" not in result.lower():
                logger.warning("В ответе отсутствует информация о проходных баллах")
                result += "\n\nℹ️ Уточните проходные баллы на сайтах вузов, так как они могут меняться"

            return result

        except httpx.TimeoutException:
            logger.error("Таймаут запроса к нейросети")
            return "⚠️ Превышено время ожидания ответа. Попробуйте сократить запрос."
        except Exception as e:
            logger.error(f"Ошибка генерации: {str(e)}")
            return "⚠️ Не удалось получить рекомендации. Проверьте введенные данные."