from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from services import change_desc

from keyboards import back_but_edit_desc
from states import EditDesc


from states import EditName

router = Router()


@router.callback_query(F.data == "edit_sub_desc")
async def send_sub_desc(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(
        f'Пожалуйста,введите новое описание для\nподписки "{data['sub_name']}"'
    )
    await state.set_state(EditDesc.desc)


@router.message(EditDesc.desc)
async def edit_name(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(desc=message.text)
    data1 = await state.get_data()
    await state.clear()
    await change_desc(data1["desc"], data1["sub_name"], session)
    await message.answer(
        f'Описание подписки успешно изменено на\n "{data1['desc']}"',
        reply_markup=back_but_edit_desc,
    )
