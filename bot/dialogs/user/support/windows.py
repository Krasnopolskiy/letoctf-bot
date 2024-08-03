from operator import attrgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Radio
from aiogram_dialog.widgets.text import Const, Format
from dialogs.user.support.states import UserSupportStateGroup
from dialogs.widgets import back
from handlers.user.support import get_support_channels, set_channel, submit

support = Window(
    Const("🆘 Напишите обращение и выберете категорию:"),
    Radio(
        Format("🔘 {item.value}"),
        Format("⚪️ {item.value}"),
        id="channel",
        item_id_getter=attrgetter("name"),
        items="channels",
        on_state_changed=set_channel,
    ),
    Cancel(back, id="back"),
    MessageInput(submit),
    state=UserSupportStateGroup.support,
    getter=get_support_channels,
)
