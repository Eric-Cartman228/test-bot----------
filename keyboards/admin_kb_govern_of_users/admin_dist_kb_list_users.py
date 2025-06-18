from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

dest_kb_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Все пользователи",
                callback_data="all_users",
            )
        ],
        [
            InlineKeyboardButton(
                text="Без подписки",
                callback_data="without_subsc",
            )
        ],
        [
            InlineKeyboardButton(
                text="С подпиской",
                callback_data="with_subsc",
            )
        ],
        [InlineKeyboardButton(text="Назад", callback_data="govern_of_users")],
    ]
)
