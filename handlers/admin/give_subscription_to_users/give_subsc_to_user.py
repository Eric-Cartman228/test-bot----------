import os

from aiogram import F, Router, types

from aiogram.types import CallbackQuery, Message

import pandas as pd

from states import GetId

from services import (
    check_func,
    chenck_func_user_name,
    get_user_id_by_username,
    get_user_id,
)

from services.admin_govern_of_user import insert_subs_from_table

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import kb_list_subscriptions, user_notification_channels

from services import insert_subs

from keyboards import (
    amount_of_days,
    back_button_for_give_subs,
    back_but_govern_of_users,
)

from states import GetDays


router = Router()


@router.callback_query(F.data == "give_subs_to_user")
async def main_menue(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        """
Пожалуйста, введите юзернайм или ID 
пользователя, либо отправьте файл с данными.
"""
    )
    await state.set_state(GetId.id)


@router.message(GetId.id)
async def get_id(message: Message, state: FSMContext, session: AsyncSession):
    from main import bot

    if not message.document:
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
                reply_markup=await kb_list_subscriptions(
                    session, list_of_chosen_tarrifs
                ),
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
                reply_markup=await kb_list_subscriptions(
                    session, list_of_chosen_tarrifs
                ),
            )
    else:
        file_name = message.document.file_name
        if not file_name.endswith(".xlsx"):
            await message.answer("Ошибка! Данный файл не является форматом excel.")
            return
        file = await bot.get_file(message.document.file_id)
        file_path = file.file_path
        dest = f"./{file_name}"
        await bot.download_file(file_path, dest)
        await message.answer("файл успешно скачан")
        file_excel = pd.read_excel(f"{file_name}")
        columns = file_excel.columns
        if not (
            (
                "Почта" in columns
                or "ФИО" in columns
                or "Телефон" in columns
                or "Юзернейм" in columns
            )
            & ("Название подписки" in columns)
            & ("Срок" in columns)
        ):
            await message.answer("Отправленная таблица неправильная!")
            os.remove(dest)
            return
        data_list = extract_data_as_list_of_dicts(file_excel)
        if data_list is None:
            await message.answer(
                "Отправленная таблица неправильная! Обязательные колонки отсутствуют."
            )
            os.remove(dest)
            return
        await insert_subs_from_table(data_list, session)
        await message.answer(
            "Подписка успешно назначена всем пользователям из файла.",
            reply_markup=back_but_govern_of_users,
        )
        for user in data_list:
            print(data_list)
            user_id = await get_user_id(user["user_value"], session)
            await send_to_user_notification(user_id, [user["sub_name"]], session)


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
    await send_to_user_notification(int(tg_id), list_of_chosen_tarrifs, session)


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
    await send_to_user_notification(int(tg_id), list_of_chosen_tarrifs, session)


def extract_data_as_list_of_dicts(df):
    """
    Преобразует DataFrame в список словарей с данными пользователя, подписки и срока.

    :param df: pandas DataFrame
    :return: tuple (list словарей, имя колонки с данными пользователя) или (None, None)
    """
    required_columns = {"Название подписки", "Срок"}
    if not required_columns.issubset(df.columns):
        return None, None

    user_columns = ["Юзернейм", "Телефон", "Почта", "ФИО"]
    user_col_name = None
    for col in user_columns:
        if col in df.columns:
            user_col_name = col
            break

    if user_col_name is None:
        return None, None

    result = []
    for _, row in df.iterrows():
        result.append(
            {
                "user_value": row[user_col_name],
                "sub_name": row["Название подписки"],
                "duration": row["Срок"],
            }
        )

    return result


async def send_to_user_notification(
    user_id: int, list_of_sub_names: list, session: AsyncSession
):
    from main import bot

    for sub in list_of_sub_names:
        await bot.send_message(
            chat_id=user_id,
            text=f"🎉 Поздравляем! Вы успешно получили подписку <b>«{sub}»</b>.\n\nТеперь у вас есть доступ к следующим каналам/группам👇:",
            parse_mode="HTML",
            reply_markup=await user_notification_channels(sub, session),
        )
