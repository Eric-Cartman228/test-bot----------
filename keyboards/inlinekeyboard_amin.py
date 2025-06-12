from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Control of subs
first_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Управление подписками", callback_data="control_of_subs"
            )
        ],
        [InlineKeyboardButton(text="Статистика", callback_data="statistics")],
        [
            InlineKeyboardButton(
                text="Управление пользователями", callback_data="govern_of_users"
            )
        ],
    ]
)
# control of users
second_inlkeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить подписку", callback_data="add_sub")],
        [
            InlineKeyboardButton(
                text="Редактировать подписку", callback_data="edit_subs"
            )
        ],
        [InlineKeyboardButton(text="Скрыть подписку", callback_data="hide_subs")],
        [
            InlineKeyboardButton(
                text="Восстановить подписку", callback_data="recover_subs"
            )
        ],
        [InlineKeyboardButton(text="Удалить подписку", callback_data="delete_subs")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")],
    ]
)
# statistics
third_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать период", callback_data="choose_period")],
        [InlineKeyboardButton(text="Выбрать подписку", callback_data="choose_subs")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")],
    ]
)

# govern of users

user_govern = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Посмотреть список пользователей",
                callback_data="look_list_of_users",
            )
        ],
        [
            InlineKeyboardButton(
                text="Назначить подписки пользователю", callback_data="give_subs"
            )
        ],
        [
            InlineKeyboardButton(
                text="удалить подписку у пользователя",
                callback_data="delete_subs_from_users",
            )
        ],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")],
    ]
)

add_another_sub = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить еще одну подписку", callback_data="add_sub"
            )
        ],
        [InlineKeyboardButton(text="Назад", callback_data="control_of_subs")],
    ]
)
