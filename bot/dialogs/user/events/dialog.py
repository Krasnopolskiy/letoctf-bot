from aiogram_dialog import Dialog
from dialogs.user.events import windows
from dispatcher import dp
from handlers.user.event import set_default_feedback_score


def events_dialog():
    dialog = Dialog(
        windows.list_events,
        windows.render,
        windows.feedback,
        on_start=set_default_feedback_score,
    )
    dp.include_router(dialog)
