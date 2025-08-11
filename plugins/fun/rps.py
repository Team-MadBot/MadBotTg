import asyncio
import random
from enum import Enum

from aiogram import Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
RPS_COOLDOWN_SECONDS = 15


class RPSOption(str, Enum):
    rock = "🪨"
    paper = "📄"
    scissors = "✂️"


class RPSCallbackData(CallbackData, prefix="rps"):
    user_id: int
    user_decision: RPSOption


class RPSStates(StatesGroup):
    user_awaiting = State()


WIN_DECISION = {
    RPSOption.rock.value: RPSOption.scissors.value,
    RPSOption.paper.value: RPSOption.rock.value,
    RPSOption.scissors.value: RPSOption.paper.value,
}


@router.message(Command("rock-paper-scissors", "rps"))
async def rpscmd(message: Message, state: FSMContext):
    """Камень-ножницы-бумага. Играйте в одиночку либо с другом, ответив на его сообщение этой командой"""
    assert message.bot is not None
    assert message.from_user is not None

    if message.reply_to_message is not None:  # TODO
        await message.reply("Я пошутил, никаких дуэлей.")
        return

    builder = InlineKeyboardBuilder()
    for option in RPSOption:
        builder.button(
            text=option.value,
            callback_data=RPSCallbackData(
                user_id=message.from_user.id, user_decision=option
            ),
        )

    msg = await message.reply(
        "<strong>Камень, ножницы, бумага</strong>\n\nНажмите на одну из кнопок ниже, чтобы сделать свой выбор. "
        f"На раздумье даётся {RPS_COOLDOWN_SECONDS} секунд.",
        parse_mode="HTML",
        reply_markup=builder.as_markup(),
    )
    await state.set_state(RPSStates.user_awaiting)
    await state.update_data(bot_msg_id=msg.message_id)
    await asyncio.sleep(RPS_COOLDOWN_SECONDS)

    data = await state.get_data()
    if data is None or data.get("bot_msg_id", 0) != msg.message_id:
        return

    await msg.edit_text("Время на принятие решения вышло.")


@router.callback_query(RPSCallbackData.filter(), RPSStates.user_awaiting)
async def handle_solo_rps_answer(
    query: types.CallbackQuery, callback_data: RPSCallbackData, state: FSMContext
):
    assert query.bot is not None
    assert isinstance(query.message, Message)

    if query.from_user.id != callback_data.user_id:
        await query.answer("Не для тебя кнопочка!", show_alert=True)
        return

    await state.clear()
    await query.answer()
    bot_answer = random.choice([op for op in RPSOption])
    user_answer = callback_data.user_decision

    if user_answer == bot_answer:
        await query.message.edit_text(f"🤝 Ничья! Вы и бот выбрали {bot_answer.value}")
        return

    if WIN_DECISION[user_answer] != bot_answer:
        await query.message.edit_text(
            f"😢 Вы проиграли! Бот выбрал {bot_answer.value}, "
            f"когда Вы выбрали {user_answer.value}"
        )
    else:
        await query.message.edit_text(
            f"🎉 Вы выиграли! Бот выбрал {bot_answer.value}, "
            f"когда Вы выбрали {user_answer.value}"
        )


async def setup(dp: Dispatcher):
    dp.include_router(router)
