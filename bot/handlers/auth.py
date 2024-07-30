from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from api.client import APIClient
from api.structs import Telegram
from database.models import User
from database.queries import find_user_by_tg_id, save_user
from dialogs.auth.states import AuthStateGroup
from dialogs.user.menu.states import UserMenuStateGroup


def telegram_link_request(message: Message) -> Telegram:
    return Telegram(
        user=message.text,
        tg_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
    )


async def check_telegram_linked(message: Message) -> User | None:
    async with APIClient() as client:
        user = await client.get_user_by_tg_id(message.from_user.id)
    if not user:
        return None
    return save_user(user_id=user.id, tg_id=message.from_user.id)


async def get_user(tg_id: int, dialog_manager: DialogManager) -> User | None:
    if user := find_user_by_tg_id(tg_id):
        return user
    await dialog_manager.start(AuthStateGroup.auth)
    return None


async def link_telegram(message: Message, _: MessageInput, dialog_manager: DialogManager):
    async with APIClient() as client:
        request = telegram_link_request(message)
        await client.link_telegram(request)
        user = await client.get_user_by_tg_id(message.from_user.id)

    if not user:
        await message.reply("❌ Токен не авторизован")
        await dialog_manager.done()
        return

    save_user(user_id=user.id, tg_id=message.from_user.id)

    await message.reply("✅ Токен авторизован")
    await dialog_manager.done()
    await dialog_manager.start(UserMenuStateGroup.menu)
