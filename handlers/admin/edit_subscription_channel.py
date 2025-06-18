from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from services import change_channel, get_channels


from keyboards import back_but
from states import EditChannel


router = Router()


@router.callback_query(F.data == "edit_sub_channel")
async def send_sub_channel(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    ls_channels = await get_channels(session)
    channels_lines = (
        f"{1+i}.Канал {i+1}: {channel}" for i, channel in enumerate(ls_channels)
    )
    text = (
        "Текущие каналы и группы для подписки\n"
        f"«{data['sub_name']}»:\n"
        + "\n".join(channels_lines)
        + "\nПожалуйста,введите ID новых каналов и групп \n через запятую,чтобы заменить текущие.И\nдобавьте этого бота в администраторы указанных\nканалов "
    )
    await callback.message.answer(text)
    await state.set_state(EditChannel.name_of_channel)


@router.message(EditChannel.name_of_channel)
async def edit_name(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(channel=message.text)
    data1 = await state.get_data()
    await state.clear()
    await change_channel(data1["channel"], data1["sub_name"], session)
    ls_channels = await get_channels(session)
    channels_lines = (
        f"{1+i}.Канал {i+1}: {channel}" for i, channel in enumerate(ls_channels)
    )
    text = (
        "Каналы и группы для подписки успешно\n"
        "обновлены.Новые каналы:\n" + "\n".join(channels_lines)
    )
    await message.answer(text, reply_markup=back_but)
