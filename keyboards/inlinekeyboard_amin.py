from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from services import (
    get_subscriptions,
    get_subscriptions_all,
    get_subscriptions_not_available,
)

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

# Builder For editing of subscriptions


async def kb_subscriptions(session: AsyncSession):
    all_subscriptions = await get_subscriptions_all(session)
    keyboard = InlineKeyboardBuilder()
    for subscription in all_subscriptions:
        keyboard.row(
            InlineKeyboardButton(
                text=subscription, callback_data=f"edit_subscriptions:{subscription}"
            )
        )
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="control_of_subs"))
    return keyboard.as_markup()


edit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Название", callback_data="edit_sub_name")],
        [InlineKeyboardButton(text="Описание", callback_data="edit_sub_desc")],
        [InlineKeyboardButton(text="Каналы/Группы", callback_data="edit_sub_channel")],
        [InlineKeyboardButton(text="Назад", callback_data="control_of_subs")],
    ]
)

back_but = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="control_of_subs")]
    ]
)


##Для скрытия подписки
async def kb_not_hide_subscriptions(session: AsyncSession):
    all_subscriptions = await get_subscriptions(session)
    keyboard = InlineKeyboardBuilder()
    for subscription in all_subscriptions:
        keyboard.row(
            InlineKeyboardButton(
                text=subscription, callback_data=f"hide_subscriptions:{subscription}"
            )
        )
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="control_of_subs"))
    return keyboard.as_markup()


# Для раскрытия подписки
async def kb_hide_subscriptions(session: AsyncSession):
    all_subscriptions = await get_subscriptions_not_available(session)
    keyboard = InlineKeyboardBuilder()
    for subscription in all_subscriptions:
        keyboard.row(
            InlineKeyboardButton(
                text=subscription, callback_data=f"make_sub_visible:{subscription}"
            )
        )
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="control_of_subs"))
    return keyboard.as_markup()


# for deleting a subscription
async def kb_delete_subscriptions(session: AsyncSession):
    all_subscriptions = await get_subscriptions_all(session)
    keyboard = InlineKeyboardBuilder()
    for subscription in all_subscriptions:
        keyboard.row(
            InlineKeyboardButton(
                text=subscription, callback_data=f"del_subscriptions:{subscription}"
            )
        )
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="control_of_subs"))
    return keyboard.as_markup()


# delete_choice
delete_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить удаление", callback_data="accept_del")],
        [InlineKeyboardButton(text="Отмена", callback_data="control_of_subs")],
    ]
)

broadcast_handler_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Посмотреть список пользователей",
                callback_data="watch_list_of_users",
            )
        ],
        [
            InlineKeyboardButton(
                text="Назначить подписки пользователю",
                callback_data="give_subs_to_user",
            )
        ],
        [
            InlineKeyboardButton(
                text="Удалить подписки у пользователя",
                callback_data="delete_subs_from_user",
            )
        ],
        [InlineKeyboardButton(text="Рассылка", callback_data="distribution")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")],
    ]
)


back_but_govern_of_users = back_but = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="govern_of_users")]
    ]
)


menue_in_list_users = back_but = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отправить файл", callback_data="send_file")],
        [InlineKeyboardButton(text="Назад", callback_data="govern_of_users")],
    ]
)
