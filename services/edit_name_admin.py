from sqlalchemy import update

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Subcription


async def change_name(new_name: str, old_name: str, session: AsyncSession):

    update_data = (
        update(Subcription).where(Subcription.name == old_name).values(name=new_name)
    )
    await session.execute(update_data)
    await session.commit()
