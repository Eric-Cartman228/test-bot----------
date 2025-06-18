from aiogram.fsm.state import State, StatesGroup


class EditDesc(StatesGroup):
    desc = State()
    secd_handler = State()
