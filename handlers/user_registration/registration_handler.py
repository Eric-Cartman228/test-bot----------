from states import UserState
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext

from aiogram.types import Message
from aiogram.filters import CommandStart

from aiogram import Router
from services import check_func, create_user


from .programms import programm_router
from .users_subscription import subscription_checker_router

from keyboards import main_kb_usesr

router = Router()


router.include_routers(programm_router, subscription_checker_router)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):

    if await check_func(message.from_user.id, session):
        await message.answer(
            "👋 Добро пожаловать! Здесь вы можете узнать о подписках на наши программы и связаться с техподдержкой для их приобретения. Выберите нужное действие:",
            reply_markup=main_kb_usesr,
        )
    else:
        await message.answer(
            "Привет! 👋 Для начала работы нам нужно собрать некоторые ваши данные. Пожалуйста, введите ваше полное имя (Ф.И.О.):"
        )
        await state.set_state(UserState.name)


@router.message(UserState.name)
async def get_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if all(part.isalpha() for part in name.split()):
        await state.update_data(name=name)
        await message.answer(
            "Спасибо! Теперь, пожалуйста, укажите ваш Email-адрес для связи:"
        )
        await state.set_state(UserState.email)
    else:
        await message.answer("Ошибка!Введите ваше имя.")


@router.message(UserState.email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Отлично! Наконец, укажите ваш номер телефона")
    await state.set_state(UserState.phone_number)


@router.message(UserState.phone_number)
async def get_phone_number(message: Message, state: FSMContext, session: AsyncSession):
    phone = message.text.strip()
    if phone.startswith("+") and phone[1:].isdigit():
        await state.update_data(phone_number=message.text)
        data = await state.get_data()
        await state.clear()
        await create_user(
            message.from_user.id,
            message.from_user.username,
            data["name"],
            data["email"],
            data["phone_number"],
            session,
        )
    else:
        await message.answer("Ошибка!Введите ваш номер телефона!")
        return
    await message.answer(
        "👋 Добро пожаловать! Здесь вы можете узнать о подписках на наши программы и связаться с техподдержкой для их приобретения. Выберите нужное действие:",
        reply_markup=main_kb_usesr,
    )
