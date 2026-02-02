from aiogram import Dispatcher, Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultsButton

router = Router()
KAOMOJIS = {
    "shrug": r"¯\_(ツ)_/¯",
    "tableflip": r"(╯°□°)╯︵ ┻━┻",
    "unflip": r"┬─┬ノ( º _ ºノ)"
}

@router.inline_query()
async def default_inline_handler(query: InlineQuery):
    await query.answer(
        [
            InlineQueryResultArticle(
                id=kaomoji,
                title=kaomoji.capitalize(),
                description=f"Добавляет {KAOMOJIS[kaomoji]} к Вашему сообщению",
                input_message_content=InputTextMessageContent(message_text=f"{query.query} {KAOMOJIS[kaomoji]}")
            ) for kaomoji in KAOMOJIS
        ],
        button=InlineQueryResultsButton(
            text="Как этим пользоваться?",
            start_parameter="inline_help"
        )
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
