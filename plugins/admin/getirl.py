import aiohttp
from aiogram import Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from config import settings

router = Router()


@router.message(Command("getirl"), F.from_user.id.in_(settings["owners"]))
async def _getirl(message: Message):
    """Проверить, есть ли человек в списке знакомых из РЖ"""
    assert message.from_user is not None
    assert message.text is not None

    args = message.text.split()[1:]

    if len(args) == 0:
        return await message.reply("Not enough arguments!")

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{settings['bot_domain']}/api/irlinfo/{args[0]}",
            headers={"Authorization": settings["apiToken"]},
        ) as resp:
            if not resp.ok:
                ans = await resp.text()
                return await message.reply(f"FAILED: {resp.status} status code!\n{ans}")
            else:
                resp_json = await resp.json()
                if not resp_json.get("isIrl", False):
                    return await message.reply("This user isn't in IRL list.")

    await message.reply("This user is in IRL list.")


async def setup(dp: Dispatcher):
    dp.include_router(router)
