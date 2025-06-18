from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from database.models import Subcription, User


async def get_all_data(session: AsyncSession):
    result = await session.execute(
        select(
            User.username,
            User.id,
            User.phone_number,
            User.email,
            Subcription.name,
            Subcription.date_activate,
            Subcription.date_expired,
        ).join(Subcription, Subcription.user_id == User.id)
    )
    all_user_data = result.all()
    return all_user_data
