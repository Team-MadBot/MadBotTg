from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("getmyid"))
async def getmyid(message: Message):
    assert message.from_user is not None

    await message.reply(
        f"Chat ID: {message.chat.id}\nYour ID: {message.from_user.id}"
        + (
            f"\nReplied user ID: {message.reply_to_message.from_user.id}"
            if message.reply_to_message and message.reply_to_message.from_user
            else ""
        )
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
