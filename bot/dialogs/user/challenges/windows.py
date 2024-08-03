from operator import attrgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Checkbox, Row, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const
from dialogs.user.challenges.states import UserChallengesStateGroup
from dialogs.widgets import back
from handlers.user.challenges import (
    can_be_submitted,
    has_assets,
    list_challenges,
    render,
    select,
    send_assets,
    submit,
    submit_hidden,
    toggle_solved,
)
from static.loader import template_widget

list_challenges = Window(
    template_widget("challenge/list"),
    ScrollingGroup(
        Select(
            template_widget("challenge/preview"),
            item_id_getter=attrgetter("id"),
            items="challenges",
            id="challenge_select",
            on_click=select,
        ),
        width=1,
        height=5,
        id="challenge_group",
    ),
    Row(
        SwitchTo(Const("🔍 Сдать скрытый флаг"), id="submit_hidden", state=UserChallengesStateGroup.submit_hidden),
    ),
    Row(
        Cancel(back, id="back"),
        Checkbox(
            Const("🙈 Скрыть решенные"),
            Const("👀 Показать решенные"),
            id="toggle_solved",
            default=False,
            on_state_changed=toggle_solved,
        ),
    ),
    getter=list_challenges,
    state=UserChallengesStateGroup.list,
)

select = Window(
    template_widget("challenge/render"),
    Button(Const("📦 Приложенные файлы"), id="assets", on_click=send_assets, when=has_assets),
    Row(
        SwitchTo(back, id="back", state=UserChallengesStateGroup.list),
        SwitchTo(
            Const("🚩 Сдать флаг"),
            id="submit",
            state=UserChallengesStateGroup.submit,
            when=can_be_submitted,
        ),
    ),
    getter=render,
    state=UserChallengesStateGroup.render,
)

submit = Window(
    Const("✍️ Введите флаг:"),
    SwitchTo(back, id="back", state=UserChallengesStateGroup.render),
    MessageInput(submit),
    state=UserChallengesStateGroup.submit,
)

submit_hidden = Window(
    Const("✍️ Введите флаг:"),
    SwitchTo(back, id="back", state=UserChallengesStateGroup.list),
    MessageInput(submit_hidden),
    state=UserChallengesStateGroup.submit_hidden,
)
