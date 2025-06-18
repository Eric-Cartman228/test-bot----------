from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.keyboard import InlineKeyboardBuilder

from services import get_subscriptions


async def kb_list_subscriptions(session: AsyncSession, chosen_tarrifs: list[str]):
    all_subscriptions = await get_subscriptions(session)
    keyboard = InlineKeyboardBuilder()
    for subscription in all_subscriptions:
        keyboard.row(
            InlineKeyboardButton(
                text=f"{'✅' if subscription in chosen_tarrifs else ''} {subscription}",
                callback_data=f"add_to_chosen_tarrifs:{subscription}",
            )
        )
    keyboard.row(InlineKeyboardButton(text="✅Готово", callback_data="ready"))
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="govern_of_users"))
    return keyboard.as_markup()


amount_of_days = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="30 дней", callback_data="30 days")],
        [InlineKeyboardButton(text="90 дней", callback_data="90 days")],
        [InlineKeyboardButton(text="180 дней", callback_data="180 days")],
        [InlineKeyboardButton(text="365 дней", callback_data="365 days")],
        [InlineKeyboardButton(text="Назад", callback_data="give_subs_to_user")],
    ]
)

back_button_for_give_subs = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="govern_of_users")]
    ]
)
