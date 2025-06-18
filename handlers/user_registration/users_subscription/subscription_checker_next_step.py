from aiogram import F, Router

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext

from keyboards import user_channel_last_kb

from services import get_channels_for_last_step

router = Router()


@router.callback_query(F.data.startswith("user_subs:"))
async def check_handler(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    sub_name = callback.data.replace("user_subs:", "")
    await state.update_data(sub_name=sub_name)
    channels = (await get_channels_for_last_step(sub_name, session))[0]
    print(channels)
    subsc = [f"{1+i}.Канал {i+1}" for i, channel in enumerate(channels)]
    text = (
        f"Подписка: {sub_name}\n\n"
        + "Включенные каналы:\n"
        + "\n".join(subsc)
        + "\n\nЧтобы перейти в соотвествующий канал,\nнажмите на кнопки ниже"
    )
    await callback.message.edit_text(
        text, reply_markup=await user_channel_last_kb(sub_name, session)
    )
