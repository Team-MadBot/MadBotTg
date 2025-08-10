from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("easteregg"))
async def easter_egg_handler(message: Message):
    """Пасхалко"""
    await message.reply("Христос воскрес!")


async def setup(dp: Dispatcher):
    dp.include_router(router)
