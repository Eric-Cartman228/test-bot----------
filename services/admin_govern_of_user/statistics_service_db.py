from database.models import User, Subcription

from sqlalchemy import select, func

from sqlalchemy.ext.asyncio import AsyncSession


async def get_statistics(session: AsyncSession):

    users_count = await session.scalar(select(func.count()).select_from(User))

    subscribers_count = await session.scalar(
        select(func.count())
        .select_from(Subcription)
        .where(Subcription.user_id.isnot(None))
    )

    ending_subs_count = await session.scalar(
        select(func.count())
        .select_from(Subcription)
        .where(Subcription.ended_sub == True)
    )

    finished_subs_count = await session.scalar(
        select(func.count()).select_from(Subcription).where(Subcription.status == False)
    )

    extended_subs_count = await session.scalar(
        select(func.count())
        .select_from(Subcription)
        .where(Subcription.extend_subs == True)
    )

    return {
        "users_count": users_count,
        "subscribers_count": subscribers_count,
        "ending_subs_count": ending_subs_count,
        "finished_subs_count": finished_subs_count,
        "extended_subs_count": extended_subs_count,
    }
