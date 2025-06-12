from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    name = State()
    email = State()
    phone_number = State()


class AddSubs(StatesGroup):
    name = State()
    description = State()
    channel_id = State()
