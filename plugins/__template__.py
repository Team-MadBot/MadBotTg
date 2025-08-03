"""This is a template for plugin files.

Plugin file MUST have async `setup` function, where you can register handlers or include routers
for the main dispatcher"""

from aiogram import Dispatcher, F, Router
from aiogram.types import Message

router = Router()


@router.message(F.migrate_to_chat_id)
async def plugin_handler_example(message: Message):
    pass


async def setup(dp: Dispatcher):
    dp.include_router(router)
