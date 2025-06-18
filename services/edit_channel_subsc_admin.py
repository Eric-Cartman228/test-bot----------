from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import update, select

from database.models import Subcription


async def change_channel(new_channel: str, sub_name: str, session: AsyncSession):
    list_of_channels = [ch.strip() for ch in new_channel.split(",")]
    update_channel = (
        update(Subcription)
        .where(Subcription.name == sub_name)
        .values(channel_id=list_of_channels)
    )
    await session.execute(update_channel)
    await session.commit()


async def get_channels(session: AsyncSession):
    old_channels = await session.scalars(select(Subcription.channel_id))
    return list(old_channels)
