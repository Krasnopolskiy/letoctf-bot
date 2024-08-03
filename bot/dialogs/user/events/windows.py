from operator import attrgetter, itemgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Radio, Row, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from dialogs.user.events.states import UserEventsStateGroup
from dialogs.widgets import back
from handlers.user.event import (
    get_feedback_data,
    has_assets,
    list_events,
    render,
    select,
    send_assets,
    set_feedback_score,
    submit_feedback,
)
from static.loader import template_widget

list_events = Window(
    template_widget("event/list"),
    ScrollingGroup(
        Select(
            template_widget("event/preview"),
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
    template_widget("event/render"),
    Button(Const("📦 Приложенные файлы"), id="assets", on_click=send_assets, when=has_assets),
    Row(
        SwitchTo(back, id="back", state=UserEventsStateGroup.list),
        SwitchTo(Const("📡 Обратная связь"), id="feedback", state=UserEventsStateGroup.feedback),
    ),
    getter=render,
    state=UserEventsStateGroup.render,
)

feedback = Window(
    Const("✍️ Чтобы отправить обратную связь, выберете оценку и напишите комментарий:"),
    Radio(
        Format("🔘 {item[0]}"),
        Format("⚪️ {item[0]}"),
        id="score",
        item_id_getter=itemgetter(1),
        items="scores",
        on_state_changed=set_feedback_score,
    ),
    Back(back, id="back"),
    MessageInput(submit_feedback),
    state=UserEventsStateGroup.feedback,
    getter=get_feedback_data,
)
