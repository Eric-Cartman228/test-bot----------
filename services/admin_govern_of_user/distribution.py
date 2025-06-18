from database.models import User, Subcription, UserSubcriptions
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_users(session: AsyncSession):
    users = await session.scalars(select(User.id))
    return users.all()


async def get_all_users_without_subc(session: AsyncSession):
    stmt = select(User.id).where(~User.subscriptions.any())
    users = await session.scalars(stmt)
    return users.all()


async def get_all_users_with_subc(session: AsyncSession):
    stmt = select(User.id).where(User.subscriptions.any())
    users = await session.scalars(stmt)
    return users.all()
