from aiogram.fsm.state import State, StatesGroup


class GetDates(StatesGroup):
    first_date = State()
    second_date = State()
