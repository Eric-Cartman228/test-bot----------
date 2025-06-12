from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

from states import AddSubs


from keyboards import add_another_sub

router = Router()


@router.callback_query(F.data == "add_sub")
async def add_sub(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста,введите название подписки:")
    await state.set_state(AddSubs.name)


@router.message(AddSubs.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отлично! Теперь введите описание подписки:")
    await state.set_state(AddSubs.description)


@router.message(AddSubs.description)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        "Отлично! Теперь добавьте этого бота в\n администаторы указанных каналов и\n отправьте ID ваших каналов через\n запятую."
    )
    await state.set_state(AddSubs.channel_id)


@router.message(AddSubs.channel_id)
async def add_channel_id(message: Message, state: FSMContext):
    await state.update_data(channel_id=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Подписка создана успешно!\n Название: Подписка для масштабирования,\n Описание: Подписка включает доступ к\n материалам и советам по масштабированию\n бизнеса и развитию проектов\n.",
        reply_markup=add_another_sub,
    )
