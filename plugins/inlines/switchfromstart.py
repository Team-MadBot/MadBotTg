from aiogram import Dispatcher, F, Router, types

router = Router()


@router.callback_query(F.data == "switch_inline_from_start")
async def switch_inline_handler(query: types.CallbackQuery):
    assert query.bot is not None
    assert query.data is not None
    assert isinstance(query.message, types.Message)

    await query.answer()
    await query.message.reply(
        "Хорошо, возвращаю. Если Вас не вернуло автоматически, нажмите кнопку ниже и выберите нужный чат.",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text="Выбрать чат", switch_inline_query="")]]
        )
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
