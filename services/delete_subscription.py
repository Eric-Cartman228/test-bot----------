from database.models import Subcription, UserSubcriptions

from sqlalchemy import delete, select

from sqlalchemy.ext.asyncio import AsyncSession


async def delete_subs(sub_name: str, session: AsyncSession):
    # Найти ID подписки
    sub_id = await session.scalar(
        select(Subcription.id).where(Subcription.name == sub_name)
    )

    if sub_id is not None:
        # Удалить все зависимости в user_subsscription
        await session.execute(
            delete(UserSubcriptions).where(UserSubcriptions.subscription_id == sub_id)
        )
        # Удалить саму подписку
        await session.execute(delete(Subcription).where(Subcription.id == sub_id))
        await session.commit()
