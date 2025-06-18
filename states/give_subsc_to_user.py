from aiogram.fsm.state import State, StatesGroup


class GetId(StatesGroup):
    id = State()


class GetDays(StatesGroup):
    days = State()
