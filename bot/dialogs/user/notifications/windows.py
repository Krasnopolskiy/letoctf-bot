from operator import attrgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const

from dialogs.user.notifications.states import UserNotificationsStateGroup
from dialogs.widgets import back
from handlers.user.notifications import has_assets, list_notifications, render, select, send_assets
from static.loader import template_widget

list_notifications = Window(
    template_widget("notification/list"),
    ScrollingGroup(
        Select(
            template_widget("notification/preview"),
            item_id_getter=attrgetter("id"),
            items="notifications",
            id="notification_select",
            on_click=select,
        ),
        width=1,
        height=5,
        id="notification_group",
    ),
    Cancel(back, id="back"),
    getter=list_notifications,
    state=UserNotificationsStateGroup.list,
)

render = Window(
    template_widget("notification/render"),
    Button(Const("📦 Приложенные файлы"), id="assets", on_click=send_assets, when=has_assets),
    SwitchTo(back, id="back", state=UserNotificationsStateGroup.list),
    getter=render,
    state=UserNotificationsStateGroup.render,
)
