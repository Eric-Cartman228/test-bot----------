from aiogram import Router, F

from aiogram.types import CallbackQuery

from services import get_all_data

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import back_but_govern_of_users

router = Router()


@router.callback_query(F.data == "watch_list_of_users")
async def getting_data(callback: CallbackQuery, session: AsyncSession):
    data = await get_all_data(session)
    user_dict = {}
    for row in data:
        key = (row[0], row[1], row[2], row[3])
        if key not in user_dict:
            user_dict[key] = []
        user_dict[key].append((row[4], row[5], row[6]))
    for i, (user_info, subs) in enumerate(user_dict.items(), start=1):
        username, user_id, phone, email = user_info
        subs_text = "\n".join(
            [
                f'- Подписка: "{s[0]}", Дата выдачи: {s[1]},\n Дата отключения: {s[2]}'
                for s in subs
            ]
        )

        await callback.message.answer(
            f"""
{i}. Пользователь: {username}
- ID пользователя: {user_id}
- Телефон: {phone}
- Gmail: {email}
{subs_text}
""",
            reply_markup=back_but_govern_of_users,
        )
