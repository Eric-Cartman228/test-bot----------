from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from database.models import Subcription, User


async def get_all_data(session: AsyncSession):
    stmt = select(
        User.username,
        User.id,
        User.phone_number,
        User.email,
        Subcription.name,
        Subcription.date_activate,
        Subcription.date_expired,
    ).outerjoin(Subcription, Subcription.user_id == User.id)
    result = await session.execute(stmt)
    all_user_data = result.all()
    return all_user_data
