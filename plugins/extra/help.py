import traceback

from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def helpcmd(message: Message):
    """[БЕТА] Список всех команд бота"""
    assert message.from_user is not None
    assert router.parent_router is not None

    cmds: list[list[str]] = []
    for i in router.parent_router.chain_tail:
        for h in i.message.handlers:
            try:
                if h.filters is None:
                    continue

                if not isinstance(h.filters[0].callback, Command):
                    continue

                l_cb: Command = h.filters[0].callback
                if h.callback.__doc__ is not None and h.callback.__doc__.startswith("[INV]"):
                    continue

                cmds += [[l_cb.commands[0], h.callback.__doc__]]
            except Exception:
                traceback.print_exc()

    cmds.sort(key=lambda x: x[0])
    txt = "<strong>Список всех команд:</strong>\n\n"
    for i in cmds:
        txt += f"/{i[0]} - {i[1] if i[1] else 'Описание отсутствует'}\n"

    await message.reply(txt, parse_mode="HTML")


async def setup(dp: Dispatcher):
    dp.include_router(router)
