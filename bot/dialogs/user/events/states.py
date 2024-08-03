from aiogram.fsm.state import State, StatesGroup


class UserEventsStateGroup(StatesGroup):
    list = State()
    render = State()
    feedback = State()
