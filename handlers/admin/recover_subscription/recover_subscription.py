from services import get_subscriptions_not_available, recover_subs

from aiogram import F, Router

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery

from keyboards import kb_hide_subscriptions

from sqlalchemy.ext.asyncio import AsyncSession

from services import recover_subs

from keyboards import (
    back_but_for_hide_subscription as back_but_for_recover_subscription,
)

router = Router()


@router.callback_query(F.data == "recover_subs")
async def recover_subs_kb(callback: CallbackQuery, session: AsyncSession):
    await callback.message.answer(
        "Выберите подписку,которую хотите\nвосстановить:",
        reply_markup=await kb_hide_subscriptions(session),
    )


@router.callback_query(F.data.startswith("make_sub_visible:"))
async def get_name_of_hidden_subsc(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    sub_name = callback.data.replace("make_sub_visible:", "")
    await recover_subs(sub_name, session)
    await state.update_data(sub_name=sub_name)
    await callback.message.answer(
        f"Подписка «{sub_name}» успешно\nвосстановлена и восстановлена и снова доступна\n пользователям.",
        reply_markup=back_but_for_recover_subscription,
    )
