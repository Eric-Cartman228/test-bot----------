from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import update, delete

from database.models import Subcription

from database.models import UserSubcriptions


async def make_null(id: int, session: AsyncSession):
    delete_row = delete(UserSubcriptions).where(UserSubcriptions.id == id)
    await session.execute(delete_row)
    await session.commit()
