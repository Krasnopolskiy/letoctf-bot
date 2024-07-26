from aiogram.fsm.state import State, StatesGroup


class UserChallengesStateGroup(StatesGroup):
    list = State()
    render = State()
    submit = State()
    submit_hidden = State()
