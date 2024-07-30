from aiogram_dialog import Dialog

from dialogs.user.events import windows
from dispatcher import dp


def events_dialog():
    dialog = Dialog(
        windows.list_events,
        windows.render,
    )
    dp.include_router(dialog)
