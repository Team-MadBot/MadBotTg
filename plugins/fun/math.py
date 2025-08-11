import asyncio
import random
import time
from typing import TypedDict

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils import markdown as aiomd

router = Router()
MATH_COOLDOWN = 5  # in seconds


class MathForm(StatesGroup):
    user_answer = State()


class MathFormData(TypedDict):
    start_time: int
    end_time: int
    problem: str
    correct_answer: int
    bot_msg_id: int
    user_answer: int


class MathFormCancel(CallbackData, prefix="math_cancel"):
    user_id: int


def check_digit(text: str) -> bool:
    try:
        int(text)
    except ValueError:
        return False
    else:
        return True


@router.message(Command("math"))
async def mathcmd(message: Message, state: FSMContext):
    """Решите математический пример за ограниченное время"""
    assert message.bot is not None
    assert message.from_user is not None

    cur_state = await state.get_state()
    if cur_state is not None:
        await message.reply(
            "Вы ещё не закончили предыдущее действие с ботом, ожидающее Вашего ответа. "
            "Закончите его, после чего Вы сможете начать играть в /math."
        )
        return

    choice = ("+", "-")
    tosolve = f"{random.randint(1, 99)} {random.choice(choice)} {random.randint(1, 99)}"
    answer = eval(tosolve)  # NOTE: unsafe shit :D
    start = time.time()
    await state.set_state(MathForm.user_answer)

    msg = await message.reply(
        "<strong>Решите пример</strong>\n\n"
        f"Сколько будет {aiomd.hcode(tosolve)}?\n\n"
        f"Ответьте на этот пример в течение {MATH_COOLDOWN:,} секунд либо нажмите кнопку ниже для отмены.",
        parse_mode="HTML",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Отмена",
                        callback_data=MathFormCancel(
                            user_id=message.from_user.id
                        ).pack(),
                    )
                ]
            ]
        ),
    )
    await state.update_data(
        start_time=start,
        problem=tosolve,
        correct_answer=answer,
        bot_msg_id=msg.message_id,
    )
    await asyncio.sleep(MATH_COOLDOWN)
    data = await state.get_data()

    if not data or data.get("bot_msg_id", 0) != msg.message_id:
        return

    await state.clear()
    await msg.edit_text(
        f"Время на решение примера вышло. Правильный ответ: {aiomd.hcode(answer)}",
        parse_mode="HTML",
    )


@router.message(MathForm.user_answer, F.text.func(check_digit))
async def handle_answer(message: Message, state: FSMContext):
    assert message.bot is not None
    assert message.text is not None

    end = time.time()
    await state.update_data(user_answer=int(message.text), end_time=end)
    data: MathFormData = await state.get_data()  # type: ignore
    await state.clear()

    await message.bot.delete_message(message.chat.id, data["bot_msg_id"])
    if data["user_answer"] == data["correct_answer"]:
        await message.reply(
            f"Ваш ответ правильный! Вы решили пример за {aiomd.hcode(round(data['end_time'] - data['start_time'], 3))} секунды.",
            parse_mode="HTML",
        )
    else:
        await message.reply(
            f"Ответ неверный! Правильный ответ: {aiomd.hcode(data['correct_answer'])}.",
            parse_mode="HTML",
        )


@router.callback_query(MathFormCancel.filter(), MathForm.user_answer)
async def cancel_math_solving(
    query: types.CallbackQuery, callback_data: MathFormCancel, state: FSMContext
):
    assert isinstance(query.message, types.Message)

    if callback_data.user_id != query.from_user.id:
        await query.answer("Не твоё дело.", show_alert=True)
        return

    await query.answer()
    await state.clear()
    await query.message.edit_text("Вы отказались от игры.")


async def setup(dp: Dispatcher):
    dp.include_router(router)
