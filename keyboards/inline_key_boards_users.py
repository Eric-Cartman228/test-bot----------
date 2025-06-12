from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

first_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⭐️Программы Школы", callback_data="school_programm"
            )
        ],
        [InlineKeyboardButton(text="✨Мои подписки", callback_data="my_subcription")],
        [
            InlineKeyboardButton(
                text="💬Связаться с тех.поддержкой", callback_data="tech.support"
            )
        ],
    ]
)
