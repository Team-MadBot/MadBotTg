from aiogram import Dispatcher, Router, F
from aiogram.types import Message

from db import ChatRepository

router = Router()


@router.message(F.migrate_to_chat_id)
@router.message(F.migrate_from_chat_id)
async def migrate_to_chat_id_handler(message: Message):
    old_id, new_id = (
        message.chat.id,
        (message.migrate_to_chat_id or message.migrate_from_chat_id),
    )
    await ChatRepository.update_chat_settings(current_chat_id=old_id, chat_id=new_id)


async def setup(dp: Dispatcher):
    dp.include_router(router)
