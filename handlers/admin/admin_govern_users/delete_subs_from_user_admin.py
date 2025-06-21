from aiogram import F, Router

from sqlalchemy import select

from database.models import Subcription, UserSubcriptions

from aiogram.types import CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext

from states import Get_Id_Username

from services import check_func, chenck_func_user_name, get_user_id_by_username

from keyboards.admin_kb_govern_of_users.delete_subsc_from_user_kb_admin import (
    delete_subsc_from_user_admin_kb,
)

from keyboards import back_but_govern_of_users

from services import make_null


router = Router()


@router.callback_query(F.data == "delete_subs_from_user")
async def check_router(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, введите юзернайм или ID пользователя:")
    await state.set_state(Get_Id_Username.Id_username)


@router.message(Get_Id_Username.Id_username)
async def get_id_username(message: Message, state: FSMContext, session: AsyncSession):
    try:
        if not await check_func(int(message.text), session):
            await message.answer("Такого пользователя нет!Введите ID заново ")
            return
        await state.clear()
        await state.update_data(id=message.text)
        data = await state.get_data()
        await message.edit_text(
            f"Текущие подписки пользователя.Выберите ту,которую хотите удалить.",
            reply_markup=await delete_subsc_from_user_admin_kb(
                int(data["id"]), session
            ),
        )
    except:
        if not await chenck_func_user_name(message.text, session):
            await message.answer("Такого пользователя нет!Введите юзернайм заново ")
            return
        await state.clear()
        id = await get_user_id_by_username(message.text, session)
        await state.update_data(id=id)
        await message.answer(
            f"Текущие подписки пользователя.Выберите ту,которую хотите удалить.",
            reply_markup=await delete_subsc_from_user_admin_kb(id, session),
        )


@router.callback_query(F.data.startswith("del_subsc_users:"))
async def get_sub_name(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    user_id = data["id"]
    sub_name = callback.data.replace("del_subsc_users:", "")
    await state.update_data(sub_name=sub_name)
    await make_null(int(sub_name), int(user_id), session)
    sub_id = int(sub_name)
    stmt = select(Subcription.name).where(Subcription.id == sub_id)
    sub_name_real = await session.scalar(stmt)
    await state.clear()
    await callback.message.edit_text(
        f"Подписка {sub_name_real} успешно удалена у пользователя",
        reply_markup=back_but_govern_of_users,
    )
    await send_user_delete_notification(sub_name_real, int(user_id), sub_id, session)


async def send_user_delete_notification(
    sub_name: str, user_id: int, sub_id: int, session: AsyncSession
):
    from main import bot

    channels_list = await get_list_of_channels(sub_name, session)
    channels_names = await format_channel_list(channels_list)
    channels_text = ", ".join(channels_names)

    await bot.send_message(
        chat_id=user_id,
        text=f"Ваша подписка <b>«{sub_name}»</b> истекла. Вы больше не имеете доступа к {channels_text}. Если хотите возобновить подписку, свяжитесь с техподдержкой.",
        parse_mode="HTML",
    )


async def get_list_of_channels(sub_name: str, session: AsyncSession):

    stmt = select(Subcription.channel_id).where(Subcription.name == sub_name)
    channels = await session.scalar(stmt)
    return channels  # channels — это list[str]


async def format_channel_list(channel_ids: list[str]):
    from main import bot

    result = []
    for channel_id in channel_ids:
        try:
            chat = await bot.get_chat(int(channel_id))
            title = chat.title or f"ID {chat.id}"
            result.append(title)
        except Exception:
            result.append(f"ID {channel_id}")
    return result
