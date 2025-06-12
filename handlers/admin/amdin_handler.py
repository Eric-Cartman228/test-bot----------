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

router = Router()

router.include_routers(sub_router)


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


@router.callback_query(F.data == "statistics")
async def control_subs(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    await callback.message.edit_text(
        "Статистику сюда кинь потом", reply_markup=stat_ad_inlinekeyboard
    )


@router.callback_query(F.data == "govern_of_users")
async def govern_of_users(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Выберите нужное действие:", reply_markup=user_govern
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
