from operator import attrgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const
from dialogs.user.events.states import UserEventsStateGroup
from dialogs.widgets import back
from handlers.user.event import has_assets, list_events, render, select, send_assets
from static.loader import load_template

list_events = Window(
    load_template("event/list"),
    ScrollingGroup(
        Select(
            load_template("event/preview"),
            item_id_getter=attrgetter("id"),
            items="events",
            id="event_select",
            on_click=select,
        ),
        width=1,
        height=5,
        id="event_group",
    ),
    Cancel(back, id="back"),
    getter=list_events,
    state=UserEventsStateGroup.list,
)

render = Window(
    load_template("event/render"),
    Button(Const("Приложенные файлы"), id="assets", on_click=send_assets, when=has_assets),
    SwitchTo(back, id="back", state=UserEventsStateGroup.list),
    getter=render,
    state=UserEventsStateGroup.render,
)
