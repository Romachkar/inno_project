from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
command_router = Router()

@command_router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет, я эхо бот")

@command_router.message(Command("help"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Список доступных команд: \n"
                         "/start - запуск бота \n"
                         "/about -краткие свединия о боте \n"
                         "/help - список всех команд")

@command_router.message(Command("about"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Пока здесь ничего нет")

@command_router.message()
async def echo_message(message: Message) -> None:
    try:
        await message.reply(text=message.text)
    except TypeError:
        await message.answer("Nice try!")
