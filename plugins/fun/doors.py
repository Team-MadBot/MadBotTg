import random

from aiogram import Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message

router = Router()


class DoorsCallback(CallbackData, prefix="doors"):
    user_id: int


@router.message(Command("doors"))
async def doorscmd(message: Message):
    assert message.bot is not None
    assert message.from_user is not None

    await message.reply(
        "<strong>Угадайте дверь</strong>\n\n"
        "Выбери одну из дверей ниже, нажав на кнопку.",
        parse_mode="HTML",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🚪",
                        callback_data=DoorsCallback(
                            user_id=message.from_user.id
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text="🚪",
                        callback_data=DoorsCallback(
                            user_id=message.from_user.id
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text="🚪",
                        callback_data=DoorsCallback(
                            user_id=message.from_user.id
                        ).pack(),
                    ),
                ]
            ]
        ),
    )


@router.callback_query(DoorsCallback.filter())
async def cancel_math_solving(query: types.CallbackQuery, callback_data: DoorsCallback):
    assert isinstance(query.message, types.Message)

    if callback_data.user_id != query.from_user.id:
        await query.answer("Не твоё дело.", show_alert=True)
        return

    await query.answer()
    if random.randint(1, 3) == 1:
        await query.message.edit_text("🎉 Вы угадали!")
    else:
        await query.message.edit_text("😢 Вы не угадали!")


async def setup(dp: Dispatcher):
    dp.include_router(router)
