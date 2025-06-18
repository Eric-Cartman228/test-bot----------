from aiogram.fsm.context import FSMContext

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession

from services import get_subscriptions, get_desc, get_channels_prog


from keyboards import kb_programms_user, main_kb_usesr, last_kb_programms

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
    sub_name = callback.data.replace("subscription_user_program:", "")
    await state.update_data(sub_name=sub_name)
    desc = await get_desc(sub_name, session)
    channels = await get_channels_prog(sub_name, session)
    channel_lines = (f"-Канал {1+i}:{channel}" for i, channel in enumerate(channels))
    text = (
        f"{sub_name}\n\n Описание:{desc}\n Включенный каналы и группы:\n"
        + "\n".join(channel_lines)
    )
    await callback.message.edit_text(text, reply_markup=last_kb_programms)


# for back button
@router.callback_query(F.data == "go_back_to_main_menu_user")
async def get_back(callback: CallbackQuery):
    await callback.message.edit_text(
        '"👋 Добро пожаловать! Здесь вы можете узнать о подписках на наши программы и связаться с техподдержкой для их приобретения. Выберите нужное действие:"',
        reply_markup=main_kb_usesr,
    )
