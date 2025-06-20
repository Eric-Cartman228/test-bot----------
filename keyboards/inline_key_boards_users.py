from sqlalchemy.ext.asyncio import AsyncSession
from services import (
    get_subscriptions,
    get_channels_for_last_step,
    get_user_subscriptions,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_kb_usesr = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⭐️Программы Школы", callback_data="programm")],
        [InlineKeyboardButton(text="✨Мои подписки", callback_data="my_subcription")],
        [
            InlineKeyboardButton(
                text="💬Связаться с тех.поддержкой",
                url="https://t.me/EvaristeGalois1811",
            )
        ],
    ]
)


# for programs of users
async def kb_programms_user(session: AsyncSession):
    all_subscriptions_visiable = await get_subscriptions(session)
    keyboard = InlineKeyboardBuilder()
    for subscription in all_subscriptions_visiable:
        keyboard.row(
            InlineKeyboardButton(
                text=subscription,
                callback_data=f"subscription_user_program:{subscription}",
            )
        )
    keyboard.row(
        InlineKeyboardButton(text="🔙Назад", callback_data="go_back_to_main_menu_user")
    )
    return keyboard.as_markup()


last_kb_programms = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Связаться с тех.поддержкой", url="https://t.me/EvaristeGalois1811"
            )
        ],
        [InlineKeyboardButton(text="🔙Назад", callback_data="programm")],
    ]
)


# user`s subscriptions
async def user_subscription_checker_kb(user_id: int, session: AsyncSession):
    all_subscriptions_visiable = await get_user_subscriptions(user_id, session)
    keyboard = InlineKeyboardBuilder()
    for subscription in all_subscriptions_visiable:
        keyboard.row(
            InlineKeyboardButton(
                text=subscription,
                callback_data=f"user_subs:{subscription}",
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text="➕Продлить подписку", url="https://t.me/EvaristeGalois1811"
        )
    )
    keyboard.row(
        InlineKeyboardButton(text="🔙Назад", callback_data="go_back_to_main_menu_user"),
    )
    return keyboard.as_markup()


user_subsc_last_kb_do_not_have_subs = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⭐️Программы Школы", callback_data="programm")],
        [
            InlineKeyboardButton(
                text="Связаться с тех.поддержкой", url="https://t.me/EvaristeGalois1811"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙Назад", callback_data="go_back_to_main_menu_user"
            )
        ],
    ]
)


async def user_channel_last_kb(name: str, session: AsyncSession):
    from main import bot

    all_channels_last_step = await get_channels_for_last_step(name, session)
    channels = all_channels_last_step[0]
    keyboard = InlineKeyboardBuilder()
    for i in range(len(channels)):
        channel = await bot.get_chat(chat_id=channels[i])
        keyboard.row(
            InlineKeyboardButton(
                text=f"Канал {i+1}",
                url=f"https://t.me/{channel.username}",
            )
        )
    keyboard.row(
        InlineKeyboardButton(text="🔙Назад", callback_data="my_subcription"),
    )
    return keyboard.as_markup()
