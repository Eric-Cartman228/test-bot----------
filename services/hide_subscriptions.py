from sqlalchemy import update


from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Subcription


async def hide_subs(sub_name: str, session: AsyncSession):

    update_status = (
        update(Subcription).where(Subcription.name == sub_name).values(status=False)
    )
    await session.execute(update_status)
    await session.commit()
