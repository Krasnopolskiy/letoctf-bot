from aiogram_dialog import Dialog
from dialogs.auth import windows
from dispatcher import dp


def auth_dialog():
    dialog = Dialog(
        windows.auth,
    )
    dp.include_router(dialog)
