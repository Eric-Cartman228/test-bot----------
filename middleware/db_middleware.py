from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from database import DatabaseHelper


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, db_helper: DatabaseHelper):
        super().__init__()
        self.db_helper = db_helper

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = self.db_helper.get_scoped_session()
        try:
            data["session"] = session
            return await handler(event, data)
        finally:
            await session.remove()