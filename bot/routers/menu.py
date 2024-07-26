from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dialogs.user.menu.states import UserMenuStateGroup
from routers.filter import authenticated


async def start_menu_dialog(_: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserMenuStateGroup.menu)


def menu_router():
    router = Router(name=__name__)
    router.message.filter(authenticated)
    router.message.register(start_menu_dialog, Command("menu"))
    return router
