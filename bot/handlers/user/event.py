import json

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import Select

from api.client import APIClient
from api.structs import Event
from config.s3 import s3
from dialogs.user.events.states import UserEventsStateGroup


def has_assets(data: dict, _: Whenable, __: DialogManager) -> bool:
    event = Event(**data)
    return len(event.files) > 0


async def list_events(**kwargs) -> dict:
    async with APIClient() as client:
        events = await client.get_events()
    return {"events": events}


async def select(_: CallbackQuery, __: Select, dialog_manager: DialogManager, item_id: str):
    async with APIClient() as client:
        event = await client.get_event(item_id)
    await dialog_manager.update({"selected": event.model_dump_json()})
    await dialog_manager.switch_to(UserEventsStateGroup.render)


async def render(dialog_manager: DialogManager, **kwargs) -> dict:
    selected = json.loads(dialog_manager.dialog_data["selected"])
    return Event(**selected).model_dump()


async def send_assets(callback: CallbackQuery, _: Button, dialog_manager: DialogManager):
    selected = json.loads(dialog_manager.dialog_data["selected"])
    event = Event(**selected)
    documents = [s3.read_document(file.s3_key) for file in event.files]
    await callback.bot.send_media_group(chat_id=callback.message.chat.id, media=documents)
