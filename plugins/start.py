from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def _start(message: Message):
    """Путеводитель для начинающих юзеров"""
    await message.reply(
        "Привет! Пока что, данный бот - лишь сырой прототип, который разрабатывается с успехом, который зависит от текущей фазы луны, магнитного поля, "
        "состояния души и других немаловажных факторов. А тут - целое ничего! Да, я серьёзно.\n\n"
        "Ознакомиться со существующими командами в боте можно, используя команду /help.",
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
