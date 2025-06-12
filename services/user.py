from database.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def check_func(tg_id: int, session: AsyncSession):
    user = await session.scalar(select(User).where(User.id == tg_id))
    print(user)
    if user == None:
        return False
    return True


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
