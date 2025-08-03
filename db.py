from typing import List
from typing import Optional

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DbBase(AsyncAttrs, DeclarativeBase):
    pass


class CaptchaChat(DbBase):
    __tablename__ = "captcha_chats"
    chat_id: Mapped[int] = mapped_column(primary_key=True)
    captcha_enabled: Mapped[bool] = mapped_column(default=False)


engine = create_async_engine("sqlite+aiosqlite:///database.db")
async_session = async_sessionmaker(engine, expire_on_commit=False)


class DatabaseManager:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(DbBase.metadata.create_all)

    @staticmethod
    async def get_session() -> async_sessionmaker[AsyncSession]:
        return async_session


class ChatRepository:
    @staticmethod
    async def create_chat(
        chat_id: int, captcha_enabled: Optional[bool] = None
    ) -> CaptchaChat:
        async with async_session() as session:
            chat = CaptchaChat(chat_id=chat_id, captcha_enabled=captcha_enabled)
            session.add(chat)
            await session.commit()
            await session.refresh(chat)
            return chat

    @staticmethod
    async def get_chat_by_id(chat_id: int) -> Optional[CaptchaChat]:
        async with async_session() as session:
            stmt = select(CaptchaChat).where(CaptchaChat.chat_id == chat_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @staticmethod
    async def update_chat_settings(current_chat_id: int, **kwargs) -> bool:
        async with async_session() as session:
            stmt = (
                update(CaptchaChat)
                .where(CaptchaChat.chat_id == current_chat_id)
                .values(**kwargs)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

    @staticmethod
    async def delete_chat(chat_id: int) -> bool:
        async with async_session() as session:
            stmt = delete(CaptchaChat).where(CaptchaChat.chat_id == chat_id)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

    @staticmethod
    async def get_all_chats() -> List[CaptchaChat]:
        async with async_session() as session:
            stmt = select(CaptchaChat)
            return list((await session.execute(stmt)).scalars().all())
