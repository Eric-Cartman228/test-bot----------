from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import InlineKeyboardButton

from services import get_users_subscriptions


async def delete_subsc_from_user_admin_kb(id: int, session: AsyncSession):
    all_subscriptions = await get_users_subscriptions(id, session)
    keyboard = InlineKeyboardBuilder()
    for subscription in all_subscriptions:
        keyboard.row(
            InlineKeyboardButton(
                text=subscription,
                callback_data=f"del_subsc_users:{subscription}",
            )
        )
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="govern_of_users"))
    return keyboard.as_markup()
