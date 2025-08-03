from aiogram import Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message

from db import ChatRepository

router = Router()


@router.message(Command("enablecaptcha"))
async def _enable_captcha(message: Message):
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
    if chat is not None and chat.captcha_enabled:
        return await message.reply(
            "Капча уже включена! Пользователи получат запрос на прохождение капчи при отправке заявки в группу "
            "(пользователи Telegram Premium принимаются сразу же). Если Вы хотите отключить вход по капче, напишите /disablecaptcha."
        )

    if chat is None:
        await ChatRepository.create_chat(chat_id=message.chat.id, captcha_enabled=True)
    else:
        await ChatRepository.update_chat_settings(
            current_chat_id=message.chat.id, captcha_enabled=True
        )

    await message.reply(
        "Включено! Теперь бот будет запрашивать капчу от пользователей, которые отправляют заявку на вход в данный чат.\n"
        "Чтобы отключить, напишите /disablecaptcha."
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
