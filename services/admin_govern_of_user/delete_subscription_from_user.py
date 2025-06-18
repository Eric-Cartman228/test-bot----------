from database.models import Subcription

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import delete


async def delete_by_id(id: int, session: AsyncSession):
    delete_subs = delete(Subcription).where(Subcription.user_id == id)
    await session.execute(delete_subs)
    await session.commit()
