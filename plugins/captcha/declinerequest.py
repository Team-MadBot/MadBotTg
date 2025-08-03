from aiogram import Dispatcher, F, Router, types

router = Router()


@router.callback_query(F.data.startswith("req_decline_"))
async def req_decline(query: types.CallbackQuery):
    assert query.bot is not None
    assert query.data is not None
    assert isinstance(query.message, types.Message)

    chat_id = query.data.removeprefix("req_decline_")
    await query.bot.decline_chat_join_request(
        chat_id=chat_id, user_id=query.from_user.id
    )
    await query.answer()
    await query.message.edit_text(
        "Ваша заявка в группу отменена. Если вдруг передумали - отправьте её ещё раз, "
        "и я вышлю Вам снова сообщение с предложением пройти капчу."
    )


async def setup(dp: Dispatcher):
    dp.include_router(router)
