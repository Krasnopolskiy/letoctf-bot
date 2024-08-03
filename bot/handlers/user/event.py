import json

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from api.client import APIClient
from api.structs import Event, SubmitFeedbackRequest
from config.s3 import s3
from dialogs.user.events.states import UserEventsStateGroup
from handlers.auth import get_user
from sqlalchemy import Select


def submit_feedback_request(message: Message, user_id: int, event_id: int, score: int) -> SubmitFeedbackRequest:
    return SubmitFeedbackRequest(
        user=user_id,
        event=event_id,
        score=score,
        text=message.text,
    )


def has_assets(data: dict, _: Whenable, __: DialogManager) -> bool:
    event = Event(**data)
    return len(event.files) > 0


async def get_feedback_data(**kwargs) -> dict:
    scores = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    return {
        "scores": scores,
        "count": len(scores),
    }


async def set_default_feedback_score(_, dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["score"] = 5
    await dialog_manager.dialog().find("score").set_checked(dialog_manager.event, 5, dialog_manager)


async def set_feedback_score(_: CallbackQuery, __, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["score"] = item_id


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


async def submit_feedback(message: Message, _: MessageInput, dialog_manager: DialogManager):
    selected = json.loads(dialog_manager.dialog_data["selected"])
    event = Event(**selected)
    user = await get_user(message.chat.id, dialog_manager=dialog_manager)
    score = int(dialog_manager.dialog_data["score"])
    request = submit_feedback_request(message, user.user_id, event.id, score)

    async with APIClient() as client:
        await client.submit_feedback(event.id, request)

    await message.reply("✅ Обратная связь отправлена")
    await dialog_manager.switch_to(UserEventsStateGroup.list)
