from aiogram import F, Router

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery


from sqlalchemy.ext.asyncio import AsyncSession

from services import delete_subs

from keyboards import (
    kb_delete_subscriptions,
    delete_choice,
    back_but_for_edit_name,
)

router = Router()


@router.callback_query(F.data == "delete_subs")
async def get_callback_delete(callback: CallbackQuery, session: AsyncSession):
    await callback.message.edit_text(
        "Выберите подписку для удаления:",
        reply_markup=await kb_delete_subscriptions(session),
    )


@router.callback_query(F.data.startswith("del_subscriptions:"))
async def get_name_of_del_sub(callback: CallbackQuery, state: FSMContext):
    sub_name = callback.data.replace("del_subscriptions:", "")
    await state.update_data(sub_name=sub_name)
    await callback.message.edit_text(
        f"""
Вы уверены,что хотите удалить подписку 
≪{sub_name}» ? Это действие
нельзя отменить.
""",
        reply_markup=delete_choice,
    )


@router.callback_query(F.data == "accept_del")
async def deleting_process(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    data = await state.get_data()
    await delete_subs(data["sub_name"], session)
    await callback.message.edit_text(
        f"""
Подписка ≪{data['sub_name']}»
успешно удалена.
""",
        reply_markup=back_but_for_edit_name,
    )
