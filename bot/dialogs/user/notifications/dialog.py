from aiogram_dialog import Dialog
from dialogs.user.notifications import windows
from dispatcher import dp


def notifications_dialog():
    dialog = Dialog(
        windows.list_notifications,
        windows.render,
    )
    dp.include_router(dialog)
