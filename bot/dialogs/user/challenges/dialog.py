from aiogram_dialog import Dialog

from dialogs.user.challenges import windows
from dispatcher import dp


def challenges_dialog():
    dialog = Dialog(
        windows.list_challenges,
        windows.select,
        windows.submit,
        windows.submit_hidden,
    )
    dp.include_router(dialog)
