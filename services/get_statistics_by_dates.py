from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, func, distinct, and_

from database.models import Subcription, User, UserSubcriptions


async def get_statistics2(date_from, date_to, session: AsyncSession):
    user_count = await session.scalar(
        select(func.count(func.distinct(UserSubcriptions.user_id))).where(
            and_(
                UserSubcriptions.date_activate >= date_from,
                UserSubcriptions.date_activate <= date_to,
            )
        )
    )

    subscriber_count = await session.scalar(
        select(func.count(func.distinct(UserSubcriptions.user_id))).where(
            and_(
                UserSubcriptions.date_activate >= date_from,
                UserSubcriptions.date_activate <= date_to,
                UserSubcriptions.user_id.isnot(None),
            )
        )
    )

    ending_sub_count = await session.scalar(
        select(func.count(func.distinct(UserSubcriptions.user_id))).where(
            and_(
                UserSubcriptions.ended_sub == True,
                UserSubcriptions.date_expired >= date_from,
                UserSubcriptions.date_expired <= date_to,
            )
        )
    )

    finished_sub_count = await session.scalar(
        select(func.count(func.distinct(UserSubcriptions.user_id))).where(
            and_(
                UserSubcriptions.date_expired >= date_from,
                UserSubcriptions.date_expired <= date_to,
            )
        )
    )

    extended_sub_count = await session.scalar(
        select(func.count(func.distinct(UserSubcriptions.user_id))).where(
            and_(
                UserSubcriptions.extend_subs == True,
                UserSubcriptions.date_activate >= date_from,
                UserSubcriptions.date_activate <= date_to,
            )
        )
    )

    return {
        "Количество пользователей": user_count or 0,
        "Количество подписчиков": subscriber_count or 0,
        "Количество завершающих подписку": ending_sub_count or 0,
        "Количество завершенных подписок": finished_sub_count or 0,
        "Количество продленных подписок": extended_sub_count or 0,
    }


async def get_stat_with_sub_name(
    date_from, date_to, sub_name: str, session: AsyncSession
):
    base_filter = and_(
        UserSubcriptions.date_activate >= date_from,
        UserSubcriptions.date_activate <= date_to,
        Subcription.name == sub_name,
    )

    user_count = await session.scalar(
        select(func.count(func.distinct(UserSubcriptions.user_id)))
        .select_from(UserSubcriptions)
        .join(Subcription, UserSubcriptions.subscription_id == Subcription.id)
        .where(base_filter)
    )

    subscriber_count = await session.scalar(
        select(func.count(func.distinct(UserSubcriptions.user_id)))
        .select_from(UserSubcriptions)
        .join(Subcription, UserSubcriptions.subscription_id == Subcription.id)
        .where(and_(base_filter, UserSubcriptions.user_id.isnot(None)))
    )

    ending_sub_count = await session.scalar(
        select(func.count(func.distinct(UserSubcriptions.user_id)))
        .select_from(UserSubcriptions)
        .join(Subcription, UserSubcriptions.subscription_id == Subcription.id)
        .where(
            and_(
                UserSubcriptions.ended_sub == True,
                UserSubcriptions.date_expired >= date_from,
                UserSubcriptions.date_expired <= date_to,
                Subcription.name == sub_name,
            )
        )
    )

    finished_sub_count = await session.scalar(
        select(func.count(func.distinct(UserSubcriptions.user_id)))
        .select_from(UserSubcriptions)
        .join(Subcription, UserSubcriptions.subscription_id == Subcription.id)
        .where(
            and_(
                UserSubcriptions.date_expired >= date_from,
                UserSubcriptions.date_expired <= date_to,
                Subcription.name == sub_name,
            )
        )
    )

    extended_sub_count = await session.scalar(
        select(func.count(func.distinct(UserSubcriptions.user_id)))
        .select_from(UserSubcriptions)
        .join(Subcription, UserSubcriptions.subscription_id == Subcription.id)
        .where(
            and_(
                UserSubcriptions.extend_subs == True,
                UserSubcriptions.date_activate >= date_from,
                UserSubcriptions.date_activate <= date_to,
                Subcription.name == sub_name,
            )
        )
    )

    return {
        "Количество пользователей": user_count or 0,
        "Количество подписчиков": subscriber_count or 0,
        "Количество завершающих подписку": ending_sub_count or 0,
        "Количество завершенных подписок": finished_sub_count or 0,
        "Количество продленных подписок": extended_sub_count or 0,
    }
