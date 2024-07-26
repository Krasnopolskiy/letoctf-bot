from aiogram.fsm.state import State, StatesGroup


class UserMenuStateGroup(StatesGroup):
    menu = State()
