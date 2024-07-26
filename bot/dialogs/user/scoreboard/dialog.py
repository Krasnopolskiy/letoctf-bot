from aiogram_dialog import Dialog
from dialogs.user.scoreboard import windows
from dispatcher import dp


def scoreboard_dialog():
    dialog = Dialog(
        windows.users,
        windows.teams,
    )
    dp.include_router(dialog)
