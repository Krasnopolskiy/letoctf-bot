from aiogram.fsm.state import State, StatesGroup


class UserNotificationsStateGroup(StatesGroup):
    list = State()
    render = State()
