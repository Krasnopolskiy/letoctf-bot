import json

from aiogram.types import CallbackQuery, Chat
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Button, Select

from api.client import APIClient
from api.structs import Notification
from config.s3 import s3
from dialogs.user.notifications.states import UserNotificationsStateGroup
from handlers.auth import get_user


def has_assets(data: dict, _: Whenable, __: DialogManager) -> bool:
    notification = Notification(**data)
    return len(notification.files) > 0


async def list_notifications(event_chat: Chat, dialog_manager: DialogManager, **kwargs) -> dict:
    user = await get_user(event_chat.id, dialog_manager=dialog_manager)
    async with APIClient() as client:
        notifications = await client.get_notifications(user.user_id)
    return {"notifications": notifications}


async def select(callback: CallbackQuery, _: Select, dialog_manager: DialogManager, item_id: str):
    user = await get_user(callback.message.chat.id, dialog_manager=dialog_manager)
    async with APIClient() as client:
        notification = await client.get_notification(item_id, user.user_id)
    await dialog_manager.update({"selected": notification.model_dump_json()})
    await dialog_manager.switch_to(UserNotificationsStateGroup.render)


async def render(dialog_manager: DialogManager, **kwargs) -> dict:
    selected = json.loads(dialog_manager.dialog_data["selected"])
    return Notification(**selected).model_dump()


async def send_assets(callback: CallbackQuery, _: Button, dialog_manager: DialogManager):
    selected = json.loads(dialog_manager.dialog_data["selected"])
    notification = Notification(**selected)
    documents = [s3.read_document(file.s3_key) for file in notification.files]
    await callback.bot.send_media_group(chat_id=callback.message.chat.id, media=documents)
