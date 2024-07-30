from aiogram_dialog import setup_dialogs

from dispatcher import dp
from routers.auth import auth_router
from routers.menu import menu_router


def register_routers():
    dp.include_router(menu_router())
    dp.include_router(auth_router())
    setup_dialogs(dp)
