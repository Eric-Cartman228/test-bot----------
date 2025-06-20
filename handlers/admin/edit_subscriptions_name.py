from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from services import change_name

from keyboards import kb_subscriptions, edit_kb_sub_name, back_but_for_edit_name

from states import EditName


router = Router()


@router.callback_query(F.data == "edit_subs")
async def list_of_subs(callback: CallbackQuery, session: AsyncSession):
    await callback.message.edit_text(
        "Выберите подписку для редактирования:",
        reply_markup=await kb_subscriptions(session),
    )


@router.callback_query(F.data.startswith("edit_subscriptions:"))
async def edit_subscription(callback: CallbackQuery, state: FSMContext):
    # sub_name = callback.data.replace("edit_subscriptions:", "")
    sub_name = callback.data.replace("edit_subscriptions:", "")
    await state.update_data(sub_name=sub_name)
    await callback.message.edit_text(
        f"Что вы хотите изменить в подписке\n«{sub_name}»",
        reply_markup=edit_kb_sub_name,
    )


@router.callback_query(F.data == "edit_sub_name")
async def send_sub_name(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(
        f'Пожалуйста,введите новое название для\nподписки "{data['sub_name']}"'
    )
    await state.set_state(EditName.name)


@router.message(EditName.name)
async def edit_name(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(name=message.text)
    data1 = await state.get_data()
    await state.clear()
    await change_name(data1["name"], data1["sub_name"], session)
    await message.answer(
        f'Название подписки успешно изменено на\n "{data1['name']}"',
        reply_markup=back_but_for_edit_name,
    )
