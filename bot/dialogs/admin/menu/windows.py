from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Start, Url
from aiogram_dialog.widgets.text import Const
from dialogs.admin.menu.states import AdminMenuStateGroup
from dialogs.admin.notifications.states import AdminNotificationsStateGroup
from dialogs.widgets import back

menu = Window(
    Const("🛠 Панель администратора, будьте осторожны"),
    Start(Const("📡 Сообщения"), id="broadcast", state=AdminNotificationsStateGroup.list),
    Url(Const("🐍 Администрирование"), Const("https://letoctf.krasnopolsky.tech/admin/"), id="admin"),
    Cancel(back, id="back"),
    state=AdminMenuStateGroup.menu,
)
