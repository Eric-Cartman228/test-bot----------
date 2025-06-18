from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import update, func, text, select

from database.models import Subcription, UserSubcriptions


async def insert_subs(
    List_of_sub_names: str, id: int, nums_days: int, session: AsyncSession
):

    for sub_name in List_of_sub_names:

        sub_id = await session.scalar(
            select(Subcription.id).where(Subcription.name == sub_name)
        )
        new_sub = UserSubcriptions(
            user_id=id,
            subscription_id=sub_id,
            date_activate=func.now(),
            date_expired=func.now() + text(f"interval'{nums_days} days'"),
        )
        # update_data = (
        #     update(Subcription)
        #     .where(Subcription.name == sub_name)
        #     .values(
        #         user_id=id,
        #         date_activate=func.now(),
        #         date_expired=func.now() + text(f"interval'{nums_days} days'"),
        #     )
        # )
        session.add(new_sub)
    await session.commit()
