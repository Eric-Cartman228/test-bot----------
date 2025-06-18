from database.models import Subcription

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select


async def get_users_subscriptions(id: int, session: AsyncSession):
    subcriptions = await session.scalars(
        select(Subcription.name).where(Subcription.user_id == id)
    )
    return subcriptions.all()
