from aiogram import Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message

from db import ChatRepository

router = Router()


@router.message(Command("disablecaptcha"))
async def _disable_captcha(message: Message):
    """Отключить одобрение заявок в группе через капчу"""
    assert message.from_user is not None

    if message.chat.type == "private":
        return await message.reply(
            "Данная функция работает только в группах, супергруппах и каналах!"
        )

    if message.from_user.id not in [
        i.user.id
        for i in (await message.chat.get_administrators())
        if isinstance(i, types.ChatMemberOwner)
    ]:
        return await message.reply("Вы не владелец группы!")

    chat = await ChatRepository.get_chat_by_id(message.chat.id)
    if chat is None or not chat.captcha_enabled:
        return await message.reply(
            "Капча уже выключена! Если Вы хотите включить вход по капче, напишите /enablecaptcha."
        )

    await ChatRepository.update_chat_settings(
        current_chat_id=message.chat.id, captcha_enabled=False
    )

    await message.reply(
        "Выключено! Теперь бот не будет запрашивать капчу от пользователей, которые отправляют заявку на вход в данный чат.\n"
        "Чтобы вернуть обратно, напишите /enablecaptcha."
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
