from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import Message
from aiogram.filters import Command

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import (
    first_ad_inlinekeyboard,
    second_ad_inlinekeyboard,
    stat_ad_inlinekeyboard,
    user_govern,
)

from sqlalchemy.ext.asyncio import AsyncSession

from .add_subs import router as sub_router
from .edit_subscriptions_name import router as edit_sub_router
from .edit_subscription_desc import router as edit_sub_desc_router
from .edit_subscription_channel import router as edit_channel_router
from .hide_subscription import router as hide_subs_router
from .recover_subscription import router as recover_router
from .delete_subscription import router as delete_router
from .admin_govern_users import main_govern_users_router
from .give_subscription_to_users import give_subs_to_user_router
from .statistics import router as statistic_router

router = Router()

router.include_routers(
    sub_router,
    edit_sub_router,
    edit_sub_desc_router,
    edit_channel_router,
    hide_subs_router,
    recover_router,
    delete_router,
    main_govern_users_router,
    give_subs_to_user_router,
    statistic_router,
)


@router.message(Command("admin"))
async def amdin_cmd(message: Message):
    await message.answer(
        "👋Добро пожаловать в админ-панель!\n Выберите действие:",
        reply_markup=first_ad_inlinekeyboard,
    )


@router.callback_query(F.data == "control_of_subs")
async def control_subs(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    await callback.message.edit_text(
        "Управление подписками", reply_markup=second_ad_inlinekeyboard
    )


@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "👋Добро пожаловать в админ-панель!\n Выберите действие:",
        reply_markup=first_ad_inlinekeyboard,
    )


@router.callback_query(F.data == "control_of_subs")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Управление подписками:",
        reply_markup=first_ad_inlinekeyboard,
    )
