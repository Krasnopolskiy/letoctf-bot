from aiogram.fsm.state import State, StatesGroup


class UserScoreboardStateGroup(StatesGroup):
    users = State()
    teams = State()
