from aiogram.types import Message

from aiogram import F, Router

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery

from keyboards import kb_not_hide_subscriptions

from sqlalchemy.ext.asyncio import AsyncSession

from services import hide_subs

from keyboards import back_but_for_hide_subscription

router = Router()


@router.callback_query(F.data == "hide_subs")
async def hide_subs_kb(callback: CallbackQuery, session: AsyncSession):
    await callback.message.edit_text(
        "Выберите подписку,которую хотите\nскрыть:",
        reply_markup=await kb_not_hide_subscriptions(session),
    )


@router.callback_query(F.data.startswith("hide_subscriptions:"))
async def get_name_of_hidden_subsc(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    sub_name = callback.data.replace("hide_subscriptions:", "")
    await hide_subs(sub_name, session)
    await state.update_data(sub_name=sub_name)
    await callback.message.edit_text(
        f"Подписка «{sub_name}»\nуспешно скрыта.Подписка будет\nнедоступна пользователям,но вся статистика сохранится. ",
        reply_markup=back_but_for_hide_subscription,
    )
