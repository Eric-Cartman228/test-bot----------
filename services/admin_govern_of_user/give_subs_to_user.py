from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import update, func, text

from database.models import Subcription


async def insert_subs(
    List_of_sub_names: str, id: int, nums_days: int, session: AsyncSession
):

    for sub_name in List_of_sub_names:
        update_data = (
            update(Subcription)
            .where(Subcription.name == sub_name)
            .values(
                user_id=id,
                date_activate=func.now(),
                date_expired=func.now() + text(f"interval'{nums_days} days'"),
            )
        )
        await session.execute(update_data)
    await session.commit()
