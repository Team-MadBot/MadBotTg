from aiogram import Dispatcher, F, Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultsButton

router = Router()

@router.inline_query(F.query == "")
async def default_inline_handler(query: InlineQuery):
    await query.answer(
        [
            InlineQueryResultArticle(
                id="shrug",
                title="Shrug",
                description=r"Добавляет ¯\_(ツ)_/¯ к Вашему сообщению",
                input_message_content=InputTextMessageContent(message_text=r"¯\_(ツ)_/¯")
            ),
            InlineQueryResultArticle(
                id="tableflip",
                title="Tableflip",
                description=r"Добавляет (╯°□°)╯︵ ┻━┻ к Вашему сообщению",
                input_message_content=InputTextMessageContent(message_text=r"(╯°□°)╯︵ ┻━┻")
            ),
            InlineQueryResultArticle(
                id="unflip",
                title="Unflip",
                description=r"Добавляет ┬─┬ノ( º _ ºノ) к Вашему сообщению",
                input_message_content=InputTextMessageContent(message_text=r"┬─┬ノ( º _ ºノ)")
            )
        ],
        button=InlineQueryResultsButton(
            text="Как этим пользоваться?",
            start_parameter="inline_help"
        )
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
