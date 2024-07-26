from aiogram_dialog import Dialog
from dialogs.user.support import windows
from dispatcher import dp
from handlers.user.support import set_default_channel


def support_dialog():
    dialog = Dialog(
        windows.support,
        on_start=set_default_channel,
    )
    dp.include_router(dialog)
