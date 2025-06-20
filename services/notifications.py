from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload

from database.models import UserSubcriptions

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.inline_key_boards_users import user_notification_channels

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import asyncio


def start_scheduler(session_maker, bot_loop):
    scheduler = AsyncIOScheduler()

    def run_in_loop():
        asyncio.run_coroutine_threadsafe(run_check(session_maker), bot_loop)

    scheduler.add_job(run_in_loop, trigger="cron", hour=21, minute=41)

    scheduler.start()


async def run_check(session_maker):
    async with session_maker() as session:
        await check_and_notify_subscriptions(session)


async def check_and_notify_subscriptions(session: AsyncSession):
    today = func.current_date()
    tomorrow = func.current_date() + text("interval '1 day'")

    stmt_soon = (
        select(UserSubcriptions)
        .options(selectinload(UserSubcriptions.subscription))
        .where(
            (UserSubcriptions.date_expired == tomorrow)
            & (UserSubcriptions.ended_sub == False)
        )
    )

    stmt_ended = (
        select(UserSubcriptions)
        .options(selectinload(UserSubcriptions.subscription))
        .where(
            (UserSubcriptions.date_expired == today)
            & (UserSubcriptions.ended_sub == False)
        )
    )

    for subs in (await session.scalars(stmt_soon)).all():
        await send_expiring_soon_notification(
            subs.user_id, subs.subscription.name, session
        )

    for subs in (await session.scalars(stmt_ended)).all():
        await send_subscription_ended_notification(
            subs.user_id, subs.subscription.name, session
        )
        subs.ended_sub = True
    await session.commit()


async def send_expiring_soon_notification(
    user_id: int, sub_name: str, session: AsyncSession
):
    from main import bot

    await bot.send_message(
        chat_id=user_id,
        text=(
            f"⏰ Внимание! Срок действия вашей подписки «{sub_name}» истекает через 1 день.\n"
            "Если вы хотите продлить подписку, пожалуйста, свяжитесь с техподдержкой как можно скорее, "
            "чтобы не потерять доступ к следующим каналам/группам👇:"
        ),
    )


async def send_subscription_ended_notification(
    user_id: int, sub_name: str, session: AsyncSession
):
    from main import bot

    await bot.send_message(
        chat_id=user_id,
        text=(
            f"❗ Ваша подписка «{sub_name}» истекла.\n"
            "Вы больше не имеете доступа к следующим каналам/группам👇:\n"
            "Если вы хотите возобновить подписку, свяжитесь с техподдержкой."
        ),
    )
