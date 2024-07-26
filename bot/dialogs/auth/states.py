from aiogram.fsm.state import State, StatesGroup


class AuthStateGroup(StatesGroup):
    auth = State()
