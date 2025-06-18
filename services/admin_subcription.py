from database.models import Subcription
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_subscription(
    name: str, description: str, session: AsyncSession, channel_id: str
):
    subcription = Subcription(
        name=name, description=description, channel_id=channel_id.split(",")
    )

    session.add(subcription)
    await session.commit()


# only for those whose status is True
async def get_subscriptions(session: AsyncSession):
    subcriptions = await session.scalars(
        select(Subcription.name).where(Subcription.status.is_(True))
    )
    return subcriptions.all()


# for all subscriptions
async def get_subscriptions_all(session: AsyncSession):
    subcriptions = await session.scalars(select(Subcription.name))
    return subcriptions.all()


# only for those whose status is False
async def get_subscriptions_not_available(session: AsyncSession):
    subcriptions = await session.scalars(
        select(Subcription.name).where(Subcription.status.is_(False))
    )
    return subcriptions.all()
