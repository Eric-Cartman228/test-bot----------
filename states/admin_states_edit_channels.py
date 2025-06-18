from aiogram.fsm.state import StatesGroup, State


class EditChannel(StatesGroup):
    name_of_channel = State()
