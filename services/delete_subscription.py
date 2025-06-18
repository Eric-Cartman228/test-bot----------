from database.models import Subcription

from sqlalchemy import delete

from sqlalchemy.ext.asyncio import AsyncSession


async def delete_subs(sub_name: str, session: AsyncSession):
    remove_subs = delete(Subcription).where(Subcription.name == sub_name)
    await session.execute(remove_subs)
    await session.commit()
