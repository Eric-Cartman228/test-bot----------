from typing import AsyncIterator
from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from core import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        self.session_maker = self.session_factory

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task
        )
        return session

    async def session_dependency(self) -> AsyncIterator[AsyncSession]:
        async with self.get_scoped_session() as session:
            yield session
            await session.remove()

    async def scoped_session_dependency(self) -> AsyncIterator[AsyncSession]:
        session = self.get_scoped_session()
        try:
            yield session
        finally:
            await session.close()


db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
