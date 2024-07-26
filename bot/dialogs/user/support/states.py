from aiogram.fsm.state import State, StatesGroup


class UserSupportStateGroup(StatesGroup):
    support = State()
