from aiogram import Dispatcher, F, Router, types
from aiogram.types import InlineQuery

router = Router()

@router.inline_query(F.query == "")
async def default_inline_handler(query: InlineQuery):
    await query.answer(
        [
            types.InlineQueryResultArticle(
                id="shrug",
                title="Shrug",
                description=r"Добавляет ¯\_(ツ)_/¯ к Вашему сообщению",
                input_message_content=types.InputTextMessageContent(message_text=r"¯\_(ツ)_/¯")
            ),
            types.InlineQueryResultArticle(
                id="tableflip",
                title="Tableflip",
                description=r"Добавляет (╯°□°)╯︵ ┻━┻ к Вашему сообщению",
                input_message_content=types.InputTextMessageContent(message_text=r"(╯°□°)╯︵ ┻━┻")
            ),
            types.InlineQueryResultArticle(
                id="unflip",
                title="Unflip",
                description=r"Добавляет ┬─┬ノ( º _ ºノ) к Вашему сообщению",
                input_message_content=types.InputTextMessageContent(message_text=r"┬─┬ノ( º _ ºノ)")
            )
        ],
        button=types.InlineQueryResultsButton(
            text="Как этим пользоваться?",
            start_parameter="inline_help"
        )
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
