from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

from config import settings

router = Router()


@router.message(Command("stop"))
async def _stop(message: Message):
    """Вызвать инфаркт у бота"""
    assert message.from_user is not None

    if message.from_user.id in settings["owners"]:
        exit()


async def setup(dp: Dispatcher):
    dp.include_router(router)
