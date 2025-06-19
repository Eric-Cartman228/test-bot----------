from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from database.models import Subcription, User, UserSubcriptions


async def get_all_data(session: AsyncSession):
    stmt = (
        select(
            User.username,
            User.id,
            User.phone_number,
            User.email,
            Subcription.name,
            UserSubcriptions.date_activate,
            UserSubcriptions.date_expired,
        )
        .outerjoin(UserSubcriptions, UserSubcriptions.user_id == User.id)
        .outerjoin(Subcription, UserSubcriptions.subscription_id == Subcription.id)
    )
    result = await session.execute(stmt)
    all_user_data = result.all()
    return all_user_data
