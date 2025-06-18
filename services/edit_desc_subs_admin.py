from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import update

from database.models import Subcription


async def change_desc(new_desc: str, sub_name: str, session: AsyncSession):
    update_desc = (
        update(Subcription)
        .where(Subcription.name == sub_name)
        .values(description=new_desc)
    )
    await session.execute(update_desc)
    await session.commit()
