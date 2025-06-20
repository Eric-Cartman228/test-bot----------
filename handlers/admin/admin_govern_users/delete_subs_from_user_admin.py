from aiogram import F, Router

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
        data = await state.get_data()
        await message.answer(
            f"Текущие подписки пользователя.Выберите ту,которую хотите удалить.",
            reply_markup=await delete_subsc_from_user_admin_kb(id, session),
        )


@router.callback_query(F.data.startswith("del_subsc_users:"))
async def get_sub_name(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    sub_name = callback.data.replace("del_subsc_users:", "")
    await state.update_data(sub_name=sub_name)
    await make_null(int(sub_name), session)
    await state.clear()
    await callback.message.edit_text(
        f"Подписка {sub_name} успешно удалена у пользователя",
        reply_markup=back_but_govern_of_users,
    )
