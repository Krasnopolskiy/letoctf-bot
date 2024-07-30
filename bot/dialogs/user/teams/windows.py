from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from dialogs.user.teams.states import UserTeamsStateGroup
from dialogs.widgets import back
from handlers.user.teams import join

join = Window(
    Const("✍️ Введите инвайт-токен:"),
    Cancel(back, id="back"),
    MessageInput(join),
    state=UserTeamsStateGroup.join,
)
