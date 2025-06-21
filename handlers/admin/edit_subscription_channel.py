from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from services import change_channel, get_channels, get_channel


from keyboards import back_but
from states import EditChannel


router = Router()


@router.callback_query(F.data == "edit_sub_channel")
async def send_sub_channel(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    from main import bot

    data = await state.get_data()
    ls_channels = await get_channel(data["sub_name"], session)
    ls_channels = ls_channels[0]
    channels_lines = []
    for i, channel in enumerate(ls_channels):
        chat = await bot.get_chat(channel)
        title = chat.title or f"ID {chat.id}"
        channels_lines.append(f"{i + 1}. Канал {i + 1}: {title}")
    text = (
        "Текущие каналы и группы для подписки\n"
        f"«{data['sub_name']}»:\n"
        + "\n".join(channels_lines)
        + "\nПожалуйста,введите ID новых каналов и групп через запятую,чтобы заменить текущие.И добавьте этого бота в администраторы указанных каналов "
    )
    await callback.message.answer(text)
    await state.set_state(EditChannel.name_of_channel)


@router.message(EditChannel.name_of_channel)
async def edit_name(message: Message, state: FSMContext, session: AsyncSession):
    from main import bot

    await state.update_data(channel=message.text)
    data1 = await state.get_data()
    await state.clear()
    await change_channel(data1["channel"], data1["sub_name"], session)
    ls_channels = await get_channel(session)
    channels_lines = (
        f"{1+i}.Канал {i+1}: {(await bot.get_chat(channel)).username}"
        for i, channel in enumerate(ls_channels)
    )
    text = (
        "Каналы и группы для подписки успешно\n"
        "обновлены.Новые каналы:\n" + "\n".join(channels_lines)
    )
    await message.answer(text, reply_markup=back_but)
