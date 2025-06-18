from aiogram import F, Router

from aiogram.types import CallbackQuery

from keyboards import broadcast_handler_kb
from keyboards.admin_kb_govern_of_users import dest_kb_user

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User

from services.admin_govern_of_user.distribution import (
    get_all_users,
    get_all_users_without_subc,
    get_all_users_with_subc,
)

from aiogram.types import CallbackQuery, Message

from states.distribution import Distribution

from aiogram.fsm.context import FSMContext

from .delete_subs_from_user_admin import router as delete_subs_from_user_router

from .get_all_data import router as get_all_data_router


router = Router()

router.include_routers(delete_subs_from_user_router, get_all_data_router)


@router.callback_query(F.data == "govern_of_users")
async def main_menue(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите нужное действие", reply_markup=broadcast_handler_kb
    )


# get destribution menu
@router.callback_query(F.data == "distribution")
async def destribution_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        """
Пожалуйста, выбрите сегмент
пользователей, которым вы хотите отправить рассылку:                                     
""",
        reply_markup=dest_kb_user,
    )


# destribution to all users


@router.callback_query(F.data == "all_users")
async def destribution_handler(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    await callback.message.answer(
        f"Вы выбрали сегмент: 'Все пользователи'.\n Пожалуйста, введите текст сообщения для рассылки."
    )
    await state.set_state(Distribution.all_users)


@router.message(Distribution.all_users)
async def broadcast_handler_users(
    message: Message, state: FSMContext, session: AsyncSession
):
    text = message.text
    users_ids = await get_all_users(session)
    await state.clear()
    successful = 0
    erros = 0
    for user_id in users_ids:
        try:
            await message.bot.send_message(user_id, text=text)
            successful += 1
        except:
            erros += 1
    await message.answer(
        f"✅Рассылка успешно отправлена {successful} пользователям из сегмента 'Все пользователи'."
    )


@router.callback_query(F.data == "without_subsc")
async def destribution_handler_without_subsc(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    await callback.message.answer(
        f"Вы выбрали сегмент: 'Пользователи без подписки'.\n Пожалуйста, введите текст сообщения для рассылки."
    )
    await state.set_state(Distribution.without_subscription)


@router.message(Distribution.without_subscription)
async def broadcast_handler_users_without_subscription(
    message: Message, state: FSMContext, session: AsyncSession
):
    text = message.text
    await state.clear()
    users_ids = await get_all_users_without_subc(session)
    successful = 0
    erros = 0
    for user_id in users_ids:
        try:
            await message.bot.send_message(user_id, text=text)
            successful += 1
        except:
            erros += 1
    await message.answer(
        f"✅Рассылка успешно отправлена {successful} пользователям из сегмента 'Пользователи без подписок'."
    )


@router.callback_query(F.data == "with_subsc")
async def destribution_handler_with_subsc(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        f"Вы выбрали сегмент: 'Пользователи подписки'.\n Пожалуйста, введите текст сообщения для рассылки."
    )
    await state.set_state(Distribution.with_subscription)


@router.message(Distribution.with_subscription)
async def broadcast_handler_users_with_subscription(
    message: Message, state: FSMContext, session: AsyncSession
):
    text = message.text
    await state.clear()
    users_ids = await get_all_users_with_subc(session)
    successful = 0
    erros = 0
    for user_id in users_ids:
        try:
            await message.bot.send_message(user_id, text=text)
            successful += 1
        except:
            erros += 1
    await message.answer(
        f"✅Рассылка успешно отправлена {successful} пользователям из сегмента 'С подпиской'."
    )
