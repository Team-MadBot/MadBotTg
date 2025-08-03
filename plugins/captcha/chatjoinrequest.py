import aiohttp

from aiogram import Dispatcher, Router, types
from aiogram.types import (
    ChatJoinRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)

from db import ChatRepository
from config import settings


router = Router()


@router.chat_join_request()
async def _join(req: ChatJoinRequest):
    assert req.bot is not None

    db_chat = await ChatRepository.get_chat_by_id(req.chat.id)
    if db_chat is None or not db_chat.captcha_enabled:
        return

    is_irl = False
    if req.chat.id == settings["mxdcxt_thoughts_id"]:
        channel = await req.bot.get_chat(settings["mxdcxt_tarahtelka_id"])
        try:
            member = await channel.get_member(req.from_user.id)
        except Exception:
            member = None
        if member is None or isinstance(member, types.ChatMemberLeft):
            await req.bot.send_message(
                req.from_user.id,
                f"Вы должны быть подписаны на привязанный к данной группе канал ({channel.invite_link}), "
                f'чтобы получить право комментировать в группе "{req.chat.title}". Подпишитесь и подайте заявку '
                "снова.",
            )
            return await req.decline()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings['bot_domain']}/api/irlinfo/{req.from_user.id}",
                headers={"Authorization": settings["apiToken"]},
            ) as resp:
                if resp.ok:
                    is_irl = (await resp.json())["isIrl"]
                else:
                    print(f"SOMETHING FAILED WHILE IRL CHECKING {req.from_user.id}")

    if (
        req.from_user.is_premium and not is_irl
    ):  # if is_irl is true, then request was sent
        return await req.bot.approve_chat_join_request(req.chat.id, req.from_user.id)

    await req.bot.send_message(
        req.from_user.id,
        f"Пожалуйста, пройдите данную капчу для проверки на бота. После этого, Вы получите доступ к чату {req.chat.title}.\n"
        "Если у Вас не работают мини-приложения, попробуйте открыть окно в веб-версии Telegram.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Капча!",
                        web_app=WebAppInfo(
                            url=f"{settings['bot_domain']}/?groupid={req.chat.id}"
                        ),
                    ),
                    InlineKeyboardButton(
                        text="Веб-версия Telegram", url="https://web.telegram.org"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Отменить запрос",
                        callback_data=f"req_decline_{req.chat.id}",
                    )
                ],
            ]
        ),
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
