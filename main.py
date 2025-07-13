import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_handlers
from dotenv import load_dotenv

load_dotenv()

telegram_bot = Bot(token=os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)

register_handlers(dispatcher)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dispatcher.start_polling(telegram_bot))