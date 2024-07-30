from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from dialogs.auth.states import AuthStateGroup
from dialogs.user.menu.states import UserMenuStateGroup
from handlers.auth import check_telegram_linked
from routers.filter import unauthenticated


async def start_auth_dialog(message: Message, dialog_manager: DialogManager):
    user = await check_telegram_linked(message)
    if user is None:
        await dialog_manager.start(AuthStateGroup.auth)
    else:
        await dialog_manager.start(UserMenuStateGroup.menu)


def auth_router():
    router = Router(name=__name__)
    router.message.filter(unauthenticated)
    router.message.register(start_auth_dialog, Command("start"))
    return router
