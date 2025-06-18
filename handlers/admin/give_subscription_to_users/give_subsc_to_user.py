import os
from aiogram import F, Router, types

from aiogram.types import CallbackQuery, Message
import pandas as pd

from states import GetId

from services import check_func, chenck_func_user_name, get_user_id_by_username

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import kb_list_subscriptions

from services import insert_subs

from keyboards import amount_of_days, back_button_for_give_subs

from states import GetDays


router = Router()


@router.callback_query(F.data == "give_subs_to_user")
async def main_menue(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        """
Пожалуйста, введите юзернайм или ID 
пользователя
"""
    )
    await state.set_state(GetId.id)


@router.message(GetId.id)
async def get_id(message: Message, state: FSMContext, session: AsyncSession):
    list_of_chosen_tarrifs = []
    try:
        if not await check_func(int(message.text), session):
            await message.answer("Такого пользователя нет!Введите заново ")
            return
        await state.clear()
        await state.update_data(id=message.text)
        await state.update_data(list_of_chosen_tarrifs=list_of_chosen_tarrifs)
        data = await state.get_data()
        await message.answer(
            f"Выберите подписки, а затем нажмите готово:",
            reply_markup=await kb_list_subscriptions(session, list_of_chosen_tarrifs),
        )
    except:
        if not await chenck_func_user_name(message.text, session):
            await message.answer("Такого пользователя нет!Введите заново ")
            return
        await state.clear()
        id = await get_user_id_by_username(message.text, session)
        await state.update_data(id=id)
        await state.update_data(list_of_chosen_tarrifs=list_of_chosen_tarrifs)
        data = await state.get_data()
        await message.answer(
            f"Выберите подписки, а затем нажмите готово:",
            reply_markup=await kb_list_subscriptions(session, list_of_chosen_tarrifs),
        )


@router.callback_query(F.data.startswith("add_to_chosen_tarrifs:"))
async def add_to_chosen_tarrifs(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    sub_name = callback.data.replace("add_to_chosen_tarrifs:", "")
    data = await state.get_data()
    list_of_chosen_tarrifs = data["list_of_chosen_tarrifs"]
    if sub_name in list_of_chosen_tarrifs:
        list_of_chosen_tarrifs.remove(sub_name)
    else:
        list_of_chosen_tarrifs.append(sub_name)
    await state.update_data(list_of_chosen_tarrifs=list_of_chosen_tarrifs)
    await callback.message.edit_text(
        f"Выберите подписки, а затем нажмите готово:",
        reply_markup=await kb_list_subscriptions(session, list_of_chosen_tarrifs),
    )


@router.callback_query(F.data == "ready")
async def ready_button(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    await callback.message.edit_text(
        "Выберите срок действия или введите вручную в виде числа",
        reply_markup=amount_of_days,
    )
    await state.set_state(GetDays.days)


@router.message(GetDays.days)
async def state_for_days(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(days=message.text)
    data = await state.get_data()
    days = data["days"]
    list_of_chosen_tarrifs = data["list_of_chosen_tarrifs"]
    tg_id = data["id"]
    await insert_subs(list_of_chosen_tarrifs, int(tg_id), int(days), session)
    await message.answer(
        f"Подписка успешно назначена пользователю на {days} дней.",
        reply_markup=back_button_for_give_subs,
    )


@router.callback_query(F.data.endswith("days"))
async def catch_days(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    nums_days = callback.data.replace("days", "")
    list_of_chosen_tarrifs = data["list_of_chosen_tarrifs"]
    tg_id = data["id"]
    await insert_subs(list_of_chosen_tarrifs, int(tg_id), int(nums_days), session)
    await state.clear()
    await callback.message.edit_text(
        f"Подписка успешно назначена пользователю на {nums_days} дней.",
        reply_markup=back_button_for_give_subs,
    )
