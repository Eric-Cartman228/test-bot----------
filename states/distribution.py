from aiogram.fsm.state import State, StatesGroup


class Distribution(StatesGroup):
    all_users = State()
    with_subscription = State()
    without_subscription = State()
