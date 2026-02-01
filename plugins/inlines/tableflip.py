from aiogram import Dispatcher, F, Router, types
from aiogram.types import InlineQuery

router = Router()
CEMOJI = r"(╯°□°)╯︵ ┻━┻"

@router.inline_query(F.query.lower().startswith("tableflip"))
async def tableflip_inline_handler(query: InlineQuery):
    try:
        _, user_message = query.query.split(maxsplit=1)
    except ValueError:
        user_message = ""
    await query.answer(
        [
            types.InlineQueryResultArticle(
                id="tableflip",
                title="Tableflip",
                description=f"Добавляет {CEMOJI} к Вашему сообщению",
                input_message_content=types.InputTextMessageContent(message_text=f"{user_message} {CEMOJI}")
            )
        ]
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
