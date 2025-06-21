from aiogram.fsm.context import FSMContext

from aiogram import Router, F

from aiogram.types import CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession

from services import get_subscriptions, get_desc, get_channels_prog

from keyboards import kb_programms_user, main_kb_usesr, last_kb_programms

from sqlalchemy import select

from database.models import Subcription

router = Router()


@router.callback_query(F.data == "programm")
async def send_massege(callback: CallbackQuery, session: AsyncSession):
    ls_subs = await get_subscriptions(session)
    sub_lines = (f"{1+i}.{sub}" for i, sub in enumerate(ls_subs))
    text = (
        "Вот доступные подписки:\n"
        + "\n".join(sub_lines)
        + "\n Выберите интересующию вас подписку,что узнать подробности"
    )
    await callback.message.edit_text(
        text, reply_markup=await kb_programms_user(session)
    )


@router.callback_query(F.data.startswith("subscription_user_program:"))
async def get_name_of_sub_programm(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    from main import bot

    sub_name = callback.data.replace("subscription_user_program:", "")
    await state.update_data(sub_name=sub_name)

    sub = await session.scalar(select(Subcription).where(Subcription.name == sub_name))
    desc = sub.description
    channels = sub.channel_id  # массив строк

    print(f"Каналы из базы: {channels}")

    channel_lines = []
    for i, channel in enumerate(channels):
        try:
            chat = await bot.get_chat(channel)
            title = chat.title or f"ID {chat.id}"
            channel_lines.append(f"- Канал {i + 1}: {title}")
        except Exception as e:
            print(f"Не удалось получить чат {channel}: {e}")
            channel_lines.append(f"- Канал {i + 1}: (не найден или нет доступа)")

    text = f"{sub_name}\n\nОписание: {desc}\nВключенные каналы и группы:\n" + "\n".join(
        channel_lines
    )
    await callback.message.edit_text(text, reply_markup=last_kb_programms)


# for back button
@router.callback_query(F.data == "go_back_to_main_menu_user")
async def get_back(callback: CallbackQuery):
    await callback.message.edit_text(
        '"👋 Добро пожаловать! Здесь вы можете узнать о подписках на наши программы и связаться с техподдержкой для их приобретения. Выберите нужное действие:"',
        reply_markup=main_kb_usesr,
    )
