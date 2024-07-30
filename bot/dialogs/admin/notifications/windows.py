from operator import attrgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const

from dialogs.admin.notifications.states import AdminNotificationsStateGroup
from dialogs.widgets import back
from handlers.admin.notifications import (
    has_assets,
    list_notifications,
    render,
    render_recipients,
    select,
    send_assets,
    send_notification,
)
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
    state=AdminNotificationsStateGroup.list,
)

render = Window(
    template_widget("notification/render"),
    Button(Const("📦 Приложенные файлы"), id="assets", on_click=send_assets, when=has_assets),
    Row(
        SwitchTo(back, id="back", state=AdminNotificationsStateGroup.list),
        SwitchTo(Const("📡 Отправить уведомление"), id="submit", state=AdminNotificationsStateGroup.render_recipients),
    ),
    getter=render,
    state=AdminNotificationsStateGroup.render,
)

render_recipients = Window(
    template_widget("notification/confirm"),
    Row(
        SwitchTo(back, id="back", state=AdminNotificationsStateGroup.render),
        Button(Const("🔥 Отправить"), id="submit", on_click=send_notification),
    ),
    getter=render_recipients,
    state=AdminNotificationsStateGroup.render_recipients,
)
