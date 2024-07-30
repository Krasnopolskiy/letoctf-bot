from aiogram.fsm.state import State, StatesGroup


class AdminNotificationsStateGroup(StatesGroup):
    list = State()
    render_recipients = State()
    render = State()
    confirm = State()
