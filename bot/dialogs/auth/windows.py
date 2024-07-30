from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from dialogs.auth.states import AuthStateGroup
from handlers.auth import link_telegram

auth = Window(
    Const("✍️ Введите инвайт-токен:"),
    MessageInput(link_telegram),
    state=AuthStateGroup.auth,
)
