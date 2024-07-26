from aiogram.types import Chat
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from api.client import APIClient
from api.structs import UserStatistics
from handlers.auth import get_user


def not_in_team(data: dict, _: Whenable, __: DialogManager) -> bool:
    statistics = UserStatistics(**data)
    return statistics.team is None


async def get_user_statistics(event_chat: Chat, **kwargs) -> dict:
    user = await get_user(event_chat.id, dialog_manager=kwargs["dialog_manager"])
    async with APIClient() as client:
        statistics = await client.get_user_statistics(user.user_id)
    return statistics.model_dump()
