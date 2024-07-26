from aiogram_dialog import Dialog
from dialogs.user.teams import windows
from dispatcher import dp


def teams_dialog():
    dialog = Dialog(
        windows.join,
    )
    dp.include_router(dialog)
