from aiogram_dialog import Dialog
from dialogs.admin.menu import windows
from dispatcher import dp


def menu_dialog():
    dialog = Dialog(
        windows.menu,
    )
    dp.include_router(dialog)
