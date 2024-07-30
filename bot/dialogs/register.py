from dialogs.admin.register import admin_dialogs
from dialogs.auth.dialogs import auth_dialog
from dialogs.user.register import user_dialogs


def register_dialogs():
    auth_dialog()
    user_dialogs()
    admin_dialogs()
