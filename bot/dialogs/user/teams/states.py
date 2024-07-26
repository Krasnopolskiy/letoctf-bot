from aiogram.fsm.state import State, StatesGroup


class UserTeamsStateGroup(StatesGroup):
    join = State()
