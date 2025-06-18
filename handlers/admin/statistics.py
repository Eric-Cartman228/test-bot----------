from aiogram import Router, F

from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import stat_ad_inlinekeyboard

from keyboards.inlinekeyboard_amin import third_inline_kb

from services.admin_govern_of_user.statistics_service_db import get_statistics

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
