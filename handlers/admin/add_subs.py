from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

from states import AddSubs

from services import create_subscription

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
        "Отлично! Теперь добавьте этого бота в администаторы указанных каналов и отправьте ID ваших каналов через запятую."
    )
    await state.set_state(AddSubs.channel_id)


@router.message(AddSubs.channel_id)
async def add_channel_id(message: Message, state: FSMContext, session: AsyncSession):
    from main import bot

    await state.update_data(channel=message.text)
    data = await state.get_data()
    channels_ids = message.text.split(",")
    for channel in channels_ids:
        try:
            channel = int(channel)
            chat = await bot.get_chat(chat_id=channel)
        except:
            return await message.answer("Неверный ID или бот недобавлен в канал!")
    await state.clear()
    await message.answer(
        f"Подписка создана успешно!\nНазвание: {data['name']},\nОписание: {data['description']}",
        reply_markup=add_another_sub,
    )
    await create_subscription(
        data["name"], data["description"], session, data["channel"]
    )
