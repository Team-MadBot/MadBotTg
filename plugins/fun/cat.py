import aiohttp
from aiogram import Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils import markdown as aiomd
from aiogram.utils.chat_action import ChatActionSender

router = Router()


@router.message(Command("cat"))
async def catcmd(message: Message):
    assert message.bot is not None
    assert message.from_user is not None

    async with ChatActionSender.upload_photo(
        chat_id=message.chat.id,
        bot=message.bot,
        message_thread_id=message.message_thread_id,
    ):
        try:
            async with aiohttp.ClientSession() as session:
                resp = await session.get(
                    "https://api.thecatapi.com/v1/images/search?mime_types=jpg,png"
                )
                json = await resp.json()

                if not resp.ok:
                    await message.reply(
                        f"Не удалось совершить запрос на сервер. Код ошибки: {aiomd.hcode(resp.status)}.",
                        parse_mode="HTML",
                    )
                    return

                await message.reply_photo(
                    types.URLInputFile(json[0]["url"]),
                    caption="Мяу!",
                    show_caption_above_media=True,
                )
        except Exception:
            await message.reply("Произошла непредвиденная ошибка. Попробуйте позже!")


async def setup(dp: Dispatcher):
    dp.include_router(router)
