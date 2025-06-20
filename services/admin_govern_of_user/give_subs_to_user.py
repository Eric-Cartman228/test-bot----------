from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import update, func, text, select

from database.models import Subcription, UserSubcriptions, User


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
        session.add(new_sub)
    await session.commit()


async def insert_subs_from_table(data_list: list, session: AsyncSession):
    for item in data_list:
        user_value = item["user_value"]
        sub_name = item["sub_name"]
        nums_days = item["duration"]
        user_id = await session.scalar(
            select(User.id).where(
                (User.username == user_value)
                | (User.phone_number == user_value)
                | (User.email == user_value)
                | (User.name == user_value)
            )
        )

        if not user_id:
            continue

        sub_id = await session.scalar(
            select(Subcription.id).where(Subcription.name == sub_name)
        )

        if not sub_id:
            continue

        new_sub = UserSubcriptions(
            user_id=user_id,
            subscription_id=sub_id,
            date_activate=func.now(),
            date_expired=func.now() + text(f"interval '{nums_days} days'"),
        )
        session.add(new_sub)

    await session.commit()


async def get_user_id(user_value: any, session: AsyncSession):
    user_id = await session.scalar(
        select(User.id).where(
            (User.username == user_value)
            | (User.phone_number == user_value)
            | (User.email == user_value)
            | (User.name == user_value)
        )
    )
    return user_id
