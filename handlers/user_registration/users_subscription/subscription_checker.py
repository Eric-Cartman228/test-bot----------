from aiogram import Router, F

from aiogram.types import CallbackQuery, Message

from services import get_user_subscriptions


from keyboards import user_subscription_checker_kb, user_subsc_last_kb_do_not_have_subs

from .subscription_checker_next_step import router as next_step_router

from sqlalchemy.ext.asyncio import AsyncSession

router = Router()

router.include_router(next_step_router)


@router.callback_query(F.data == "my_subcription")
async def my_subsc(callback: CallbackQuery, session: AsyncSession):

    user_subscriptions_result = await get_user_subscriptions(
        callback.from_user.id, session
    )
    if user_subscriptions_result:
        subsc = [f"{1+i}.{sub}" for i, sub in enumerate(user_subscriptions_result)]
        text = (
            "👋Приветствуем! У Вас активна подписка на:\n"
            + "\n".join(subsc)
            + "\nВыберите подписку, чтобы увидеть ее детали"
        )

        await callback.message.edit_text(
            text,
            reply_markup=await user_subscription_checker_kb(
                callback.from_user.id, session
            ),
        )

    else:
        await callback.message.edit_text(
            """
😕У вас нет активных подписок на 
данный момент. 
Чтобы ознакомиться с доступными 
подписками, перейдите по кнопке 
"Подписки Школы". Если у вас есть вопросы или вам 
нужна помощь с оформлением подписки, свяжитесь с 
нашей тех.поддержкой
""",
            reply_markup=user_subsc_last_kb_do_not_have_subs,
        )
