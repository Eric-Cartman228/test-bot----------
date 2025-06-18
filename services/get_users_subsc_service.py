from database.models import Subcription, UserSubcriptions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_users_subscriptions(id: int, session: AsyncSession):
    stmt = (
        select(Subcription)
        .join(UserSubcriptions, Subcription.id == UserSubcriptions.subscription_id)
        .where(UserSubcriptions.user_id == id)
    )
    result = await session.scalars(stmt)
    return result.all()
