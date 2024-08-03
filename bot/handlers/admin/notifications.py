import asyncio
import json

import jinja2
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Button, Select
from api.client import APIClient
from api.structs import Notification
from config.bot import bot
from config.s3 import s3
from database.queries import find_user_by_id
from dialogs.admin.notifications.states import AdminNotificationsStateGroup
from static.loader import template_text

environment = jinja2.Environment()


def has_assets(data: dict, _: Whenable, __: DialogManager) -> bool:
    notification = Notification(**data)
    return len(notification.files) > 0


async def list_notifications(**kwargs) -> dict:
    async with APIClient() as client:
        notifications = await client.get_notifications_staff()
    return {"notifications": notifications}


async def select(_: CallbackQuery, __: Select, dialog_manager: DialogManager, item_id: str):
    async with APIClient() as client:
        notification = await client.get_notification_staff(item_id)
    await dialog_manager.update({"selected": notification.model_dump_json()})
    await dialog_manager.switch_to(AdminNotificationsStateGroup.render_recipients)


async def render(dialog_manager: DialogManager, **kwargs) -> dict:
    selected = json.loads(dialog_manager.dialog_data["selected"])
    return Notification(**selected).model_dump()


async def render_recipients(dialog_manager: DialogManager, **kwargs) -> dict:
    selected = json.loads(dialog_manager.dialog_data["selected"])
    notification = Notification(**selected)
    async with APIClient() as client:
        recipients = await client.get_notification_recipients(notification.id)
    return {"notification": selected, "recipients": recipients}


async def send_assets(callback: CallbackQuery, _: Button, dialog_manager: DialogManager):
    selected = json.loads(dialog_manager.dialog_data["selected"])
    notification = Notification(**selected)
    documents = [s3.read_document(file.s3_key) for file in notification.files]
    await callback.bot.send_media_group(chat_id=callback.message.chat.id, media=documents)


async def send_notification(callback: CallbackQuery, __: Button, dialog_manager: DialogManager):
    selected = json.loads(dialog_manager.dialog_data["selected"])
    notification = Notification(**selected)
    async with APIClient() as client:
        recipients = await client.get_notification_recipients(notification.id)
    for recipient in recipients:
        if not (user := find_user_by_id(recipient.id)):
            continue
        message = template_text("notification/render", notification.model_dump())
        await bot.bot.send_message(user.tg_id, message)
        await asyncio.sleep(0.5)
    await callback.message.answer("✅ Рассылка отправлена")
    await dialog_manager.done()
