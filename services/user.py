from database.models import User
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Subcription, UserSubcriptions


async def check_func(tg_id: int, session: AsyncSession):
    user = await session.scalar(select(User).where(User.id == tg_id))
    print(user)
    if user == None:
        return False
    return True


async def chenck_func_user_name(user_name: str, session: AsyncSession):
    user_id = await session.scalar(select(User.id).where(User.username == user_name))
    if user_id == None:
        return False
    return True


async def get_user_id_by_username(username: str, session: AsyncSession):

    return await session.scalar(select(User.id).where(User.username == username))


async def create_user(
    tg_id: int,
    username: str,
    name: str,
    email: str,
    phone_num: str,
    session: AsyncSession,
):
    user = User(
        id=tg_id, name=name, email=email, phone_number=phone_num, username=username
    )

    session.add(user)
    await session.commit()


# To take description from table Subscription
async def get_desc(name: str, session: AsyncSession):
    desc = await session.scalar(
        select(Subcription.description).where(Subcription.name == name)
    )

    return desc


# To take channels from table Subscription
async def get_channels_prog(name: str, session: AsyncSession):
    channels = await session.scalar(
        select(Subcription.channel_id).where(Subcription.name == name)
    )

    return channels


# to get user`s subscriptions
async def get_user_subscriptions(id: int, session: AsyncSession):
    stmt = (
        select(Subcription.name)
        .join(UserSubcriptions, Subcription.id == UserSubcriptions.subscription_id)
        .where(
            UserSubcriptions.user_id == id,
            UserSubcriptions.ended_sub == False,
            UserSubcriptions.date_activate <= func.current_date(),
            UserSubcriptions.date_expired >= func.current_date(),
        )
    )
    result = await session.scalars(stmt)
    return result.all()


# to get channels for user last step
async def get_channels_for_last_step(sub_name: str, session: AsyncSession):
    subscriptions = await session.scalars(
        select(Subcription.channel_id).where(Subcription.name == sub_name)
    )
    return subscriptions.all()
