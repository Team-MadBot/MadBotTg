import random

from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("8ball"))
async def ballcmd(message: Message):
    """Магический шар. Задайте свой вопрос - а шар даст Вам ответ"""
    assert message.bot is not None
    assert message.from_user is not None

    if len(message.md_text.split()) <= 1:
        await message.reply(
            "Укажите свой вопрос в команде!\n"
            "Пример: <code>/8ball MadBot v2 soon?</code>",
            parse_mode="HTML"
        )
        return

    user_question = message.md_text.removeprefix("/8ball ")
    answers = (
            "Бесспорно",
            "Предрешено",
            "Никаких сомнений",
            "Определённо да",
            "Можешь быть уверен в этом",
            "Мне кажется — «да»",
            "Вероятнее всего",
            "Хорошие перспективы",
            "Знаки говорят — «да»",
            "Да",
            "Пока не ясно, попробуй снова",
            "Спроси позже",
            "Лучше не рассказывать",
            "Сейчас нельзя предсказать",
            "Сконцентрируйся и спроси опять",
            "Даже не думай",
            "Мой ответ — «нет»",
            "По моим данным — «нет»",
            "Перспективы не очень хорошие",
            "Весьма сомнительно",
        )

    await message.reply(
        "*Магический шар*\n\n"
        f"*Ваш вопрос:*\n{user_question}\n\n*Ответ шара:*\n{random.choice(answers)}",
        parse_mode="MarkdownV2"
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
