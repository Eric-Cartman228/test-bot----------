from aiogram import Router, F

from keyboards import menue

from aiogram.types import CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from keyboards import stat_ad_inlinekeyboard

from aiogram.fsm.context import FSMContext

from keyboards.inlinekeyboard_amin import third_inline_kb, statistic_kb_builder

from services.admin_govern_of_user.statistics_service_db import get_statistics

from services import get_statistics2, get_stat_with_sub_name

from states import GetDates

router = Router()


@router.callback_query(F.data == "statistics")
async def control_subs1(callback: CallbackQuery, session: AsyncSession):
    stats = await get_statistics(session)
    await callback.message.answer(
        f"Количество пользователей: {stats['users_count']}\n"
        f"Количество подписчиков: {stats['subscribers_count']}\n"
        f"Количество завершающих подписку: {stats['ending_subs_count']}\n"
        f"Количество завершенных подписок: {stats['finished_subs_count']}\n"
        f"Количество продленных подписок: {stats['extended_subs_count']}",
        reply_markup=third_inline_kb,
    )


@router.callback_query(F.data == "choose_period")
async def choose_period(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите первую дату:")
    await state.set_state(GetDates.first_date)


@router.message(GetDates.first_date)
async def get_first_date(message: Message, state: FSMContext):
    try:
        date_obj = datetime.strptime(message.text, "%Y-%m-%d").date()
        first_date = await state.update_data(first_date=date_obj)
        await message.answer("Выберите вторую дату:")
        await state.set_state(GetDates.second_date)
    except ValueError:
        await message.answer(
            "❗ Неверный формат даты. Введите в формате ГГГГ-ММ-ДД (например 2024-01-02)."
        )


@router.message(GetDates.second_date)
async def get_second_date(message: Message, state: FSMContext, session: AsyncSession):
    try:
        date_obj = datetime.strptime(message.text, "%Y-%m-%d").date()
        second_date = await state.update_data(second_date=date_obj)
        data = await state.get_data()
        data_sub_stat_name = data.get("sub_name_statistic")
        if not data_sub_stat_name:
            stats = await get_statistics2(
                data["first_date"], data["second_date"], session
            )
        else:
            stats = await get_stat_with_sub_name(
                data["first_date"], data["second_date"], data_sub_stat_name, session
            )
        text = "\n".join([f"{k}: {v}" for k, v in stats.items()])
        await message.answer(
            f"📊 Статистика за выбранный период:\n{text}", reply_markup=menue
        )
        await state.clear()
    except ValueError:
        await message.answer(
            "❗ Неверный формат даты. Введите в формате ГГГГ-ММ-ДД (например 2024-01-02)."
        )


@router.callback_query(F.data == "choose_subs")
async def choose_subs(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    await callback.message.answer(
        "Выберите параметры расширенной статистики за период:",
        reply_markup=await statistic_kb_builder(session),
    )


@router.callback_query(F.data.startswith("stat_kb_sub:"))
async def get_sub_name(callback: CallbackQuery, state: FSMContext):
    sub_name = callback.data.replace("stat_kb_sub:", "")
    await state.update_data(sub_name_statistic=sub_name)
    await callback.message.answer("Выберете первую дату")
    await state.set_state(GetDates.first_date)
