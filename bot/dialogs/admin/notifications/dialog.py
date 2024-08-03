from aiogram_dialog import Dialog
from dialogs.admin.notifications import windows
from dispatcher import dp


def notifications_dialog():
    dialog = Dialog(
        windows.list_notifications,
        windows.render,
        windows.render_recipients,
    )
    dp.include_router(dialog)
