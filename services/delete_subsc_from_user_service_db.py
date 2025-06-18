from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import update

from database.models import Subcription


async def make_null(sub_name: str, session: AsyncSession):
    update_to_null = (
        update(Subcription)
        .where(Subcription.name == sub_name)
        .values(user_id=None, date_activate=None, date_expired=None)
    )
    await session.execute(update_to_null)
    await session.commit()
