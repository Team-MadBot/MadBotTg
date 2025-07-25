import asyncio
import logging
import sqlite3

import aiogram
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import (
    ChatJoinRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from config import settings

BOT_TOKEN = settings["token"]
API_TOKEN = settings["apiToken"]

dp = Dispatcher()
db = sqlite3.connect("database.db", autocommit=True)
db.row_factory = sqlite3.Row
cur = db.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS captcha_chats (
        chat_id INTEGER NOT NULL,
        captcha_enabled INTEGER NOT NULL DEFAULT(0)
    );"""
)


@dp.message(F.migrate_to_chat_id)
@dp.message(F.migrate_from_chat_id)
async def migrate_to_chat_id_handler(message: Message):
    old_id, new_id = (
        message.chat.id,
        (message.migrate_to_chat_id or message.migrate_from_chat_id),
    )
    cur.execute(
        """UPDATE captcha_chats SET chat_id = ? WHERE chat_id = ?""", (new_id, old_id)
    )


@dp.message(Command("easteregg"))
async def easter_egg_handler(message: Message):
    await message.reply("Христос воскрес!")


@dp.message(Command("enablecaptcha"))
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

    cur.execute("""SELECT * FROM captcha_chats WHERE chat_id = ?""", (message.chat.id,))
    chat = cur.fetchone()
    if chat is not None and chat["captcha_enabled"]:
        return await message.reply(
            "Капча уже включена! Пользователи получат запрос на прохождение капчи при отправке заявки в группу "
            "(пользователи Telegram Premium принимаются сразу же). Если Вы хотите отключить вход по капче, напишите /disablecaptcha."
        )

    if chat is None:
        cur.execute(
            """INSERT INTO captcha_chats (chat_id, captcha_enabled) VALUES (?, ?)""",
            (message.chat.id, 1),
        )
    else:
        cur.execute(
            """UPDATE captcha_chats SET captcha_enabled = ? WHERE chat_id = ?""",
            (1, message.chat.id),
        )

    await message.reply(
        "Включено! Теперь бот будет запрашивать капчу от пользователей, которые отправляют заявку на вход в данный чат.\n"
        "Чтобы отключить, напишите /disablecaptcha."
    )


@dp.message(Command("disablecaptcha"))
async def _disable_captcha(message: Message):
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

    cur.execute("""SELECT * FROM captcha_chats WHERE chat_id = ?""", (message.chat.id,))
    chat = cur.fetchone()
    if chat is None or not chat["captcha_enabled"]:
        return await message.reply(
            "Капча уже выключена! Если Вы хотите включить вход по капче, напишите /enablecaptcha."
        )

    cur.execute(
        """UPDATE captcha_chats SET captcha_enabled = ? WHERE chat_id = ?""",
        (0, message.chat.id),
    )

    await message.reply(
        "Выключено! Теперь бот не будет запрашивать капчу от пользователей, которые отправляют заявку на вход в данный чат.\n"
        "Чтобы вернуть обратно, напишите /enablecaptcha."
    )


@dp.message(Command("getmyid"))
async def getmyid(message: Message):
    assert message.from_user is not None

    await message.reply(
        f"Chat ID: {message.chat.id}\nYour ID: {message.from_user.id}"
        + f"\nReplied user ID: {message.reply_to_message.from_user.id}"
        if message.reply_to_message and message.reply_to_message.from_user
        else ""
    )


@dp.message(Command("stop"))
async def _stop(message: Message):
    assert message.from_user is not None

    if message.from_user.id in settings["owners"]:
        exit()


@dp.message(Command("addirl"))
async def _addirl(message: Message):
    assert message.from_user is not None
    assert message.text is not None

    if message.from_user.id not in settings["owners"]:
        return

    args = message.text.split()[1:]

    if len(args) == 0:
        return await message.reply("Not enough arguments!")

    async with aiohttp.ClientSession() as session:
        async with session.put(
            f"{settings['bot_domain']}/api/irlinfo/{args[0]}",
            headers={"Authorization": API_TOKEN},
        ) as resp:
            if not resp.ok:
                ans = await resp.text()
                return await message.reply(f"FAILED: {resp.status} status code!\n{ans}")

    await message.reply("done")


@dp.message(Command("removeirl"))
async def _removeirl(message: Message):
    assert message.from_user is not None
    assert message.text is not None

    if message.from_user.id not in settings["owners"]:
        return

    args = message.text.split()[1:]

    if len(args) == 0:
        return await message.reply("Not enough arguments!")

    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"{settings['bot_domain']}/api/irlinfo/{args[0]}",
            headers={"Authorization": API_TOKEN},
        ) as resp:
            if not resp.ok:
                ans = await resp.text()
                return await message.reply(f"FAILED: {resp.status} status code!\n{ans}")

    await message.reply("done")


@dp.message(Command("getirl"))
async def _getirl(message: Message):
    assert message.from_user is not None
    assert message.text is not None

    if message.from_user.id not in settings["owners"]:
        return

    args = message.text.split()[1:]

    if len(args) == 0:
        return await message.reply("Not enough arguments!")

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{settings['bot_domain']}/api/irlinfo/{args[0]}",
            headers={"Authorization": API_TOKEN},
        ) as resp:
            if not resp.ok:
                ans = await resp.text()
                return await message.reply(f"FAILED: {resp.status} status code!\n{ans}")
            else:
                resp_json = await resp.json()
                if not resp_json.get("isIrl", False):
                    return await message.reply("This user isn't in IRL list.")

    await message.reply("This user is in IRL list.")


@dp.message(Command("community", "comm"))
async def _community(message: Message):
    await message.reply("Ссылка: https://discord.gg/DvYPRm939R")


@dp.message(Command("group", "grouptg"))
async def _group(message: Message):
    await message.reply("Ссылка: https://t.me/MadCat9958Group")


@dp.message(Command("start", "help"))
async def _start(message: Message):
    await message.reply(
        "Привет! Пока что, данный бот - лишь сырой прототип, который разрабатывается с успехом, который зависит от текущей фазы луны, магнитного поля, "
        "состояния души и других немаловажных факторов. А тут - целое ничего! Да, я серьёзно.",
    )


@dp.chat_join_request()
async def _join(req: ChatJoinRequest):
    assert req.bot is not None

    cur.execute("SELECT * FROM captcha_chats WHERE chat_id = ?", (req.chat.id,))
    db_chat = cur.fetchone()
    if db_chat is None or not db_chat["captcha_enabled"]:
        return

    is_irl = False
    if -1002479902734 == req.chat.id:
        channel = await req.bot.get_chat(-1002400604156)
        try:
            member = await channel.get_member(req.from_user.id)
        except:  # noqa
            member = None
        if member is None or isinstance(member, aiogram.types.ChatMemberLeft):
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


@dp.callback_query(F.data.startswith("req_decline_"))
async def req_decline(query: types.CallbackQuery):
    await query.answer(
        "Пока что, это лишь заглушка. Скоро функционал будет реализован ✨",
        show_alert=True,
    )


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
