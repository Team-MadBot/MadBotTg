import aiohttp

from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config import settings

router = Router()


@router.message(Command("removeirl"), F.from_user.id.in_(settings["owners"]))
async def _removeirl(message: Message):
    """[INV] Убрать пользователя из списка знакомых в РЖ"""
    assert message.from_user is not None
    assert message.text is not None

    args = message.text.split()[1:]

    if len(args) == 0:
        return await message.reply("Not enough arguments!")

    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"{settings['bot_domain']}/api/irlinfo/{args[0]}",
            headers={"Authorization": settings["apiToken"]},
        ) as resp:
            if not resp.ok:
                ans = await resp.text()
                return await message.reply(f"FAILED: {resp.status} status code!\n{ans}")

    await message.reply("done")


async def setup(dp: Dispatcher):
    dp.include_router(router)
