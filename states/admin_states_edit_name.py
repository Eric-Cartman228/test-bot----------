from aiogram.fsm.state import State, StatesGroup


class EditName(StatesGroup):

    name = State()
    send_to_secd_hand = State()
