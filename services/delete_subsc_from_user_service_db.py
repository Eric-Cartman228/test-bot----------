from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import update, delete

from database.models import Subcription

from database.models import UserSubcriptions


async def make_null(id: int, user_id: int, session: AsyncSession):
    delete_row = delete(UserSubcriptions).where(
        (UserSubcriptions.user_id == user_id) & (UserSubcriptions.subscription_id == id)
    )
    await session.execute(delete_row)
    await session.commit()
