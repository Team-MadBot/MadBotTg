from aiogram import Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def _start(message: Message):
    """Путеводитель для начинающих юзеров"""
    if message.text == "/start inline_help":
        await message.reply(
            "<strong>Как пользоваться инлайн-режимом?</strong>\n\n"
            "Чтобы написать сообщение с добавлением каомодзи в конце сообщения, введите Ваше сообщение, "
            "а затем выберите в меню желаемый каомодзи.\n\n<strong>Пример:</strong> <code>Привет, мир</code> "
            "превратится в <code>Привет, мир ¯\\_(ツ)_/¯</code>, если выбрать Shrug.",
            parse_mode="html",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(text="Вернуться обратно", callback_data="switch_inline_from_start")]
                ]
            )
        )
        return

    await message.reply(
        "Привет! Пока что, данный бот - лишь сырой прототип, который разрабатывается с успехом, который зависит от текущей фазы луны, магнитного поля, "
        "состояния души и других немаловажных факторов. А тут - целое ничего! Да, я серьёзно.\n\n"
        "Ознакомиться со существующими командами в боте можно, используя команду /help.",
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
