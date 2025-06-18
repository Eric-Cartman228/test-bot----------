from database.models import User, Subcription, UserSubcriptions

from sqlalchemy import select, func

from sqlalchemy.ext.asyncio import AsyncSession


async def get_statistics(session: AsyncSession):

    users_count = await session.scalar(select(func.count()).select_from(User))

    subscribers_count = await session.scalar(
        select(func.count())
        .select_from(UserSubcriptions)
        .where(UserSubcriptions.user_id.isnot(None))
    )

    ending_subs_count = await session.scalar(
        select(func.count())
        .select_from(UserSubcriptions)
        .where(UserSubcriptions.ended_sub == True)
    )

    finished_subs_count = await session.scalar(
        select(func.count()).select_from(UserSubcriptions)
    )

    extended_subs_count = await session.scalar(
        select(func.count())
        .select_from(UserSubcriptions)
        .where(UserSubcriptions.extend_subs == True)
    )

    return {
        "users_count": users_count,
        "subscribers_count": subscribers_count,
        "ending_subs_count": ending_subs_count,
        "finished_subs_count": finished_subs_count,
        "extended_subs_count": extended_subs_count,
    }
