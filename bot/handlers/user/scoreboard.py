from aiogram.types import Chat
from aiogram_dialog import DialogManager

from api.client import APIClient
from handlers.auth import get_user


async def render_users(event_chat: Chat, dialog_manager: DialogManager, **kwargs) -> dict:
    current_user = await get_user(event_chat.id, dialog_manager=dialog_manager)
    async with APIClient() as client:
        users = await client.get_users_scoreboard()
    place = next((place + 1 for place, user in enumerate(users) if user.id == current_user.user_id), "∞")
    return {"users": users, "place": place}


async def render_teams(event_chat: Chat, dialog_manager: DialogManager, **kwargs) -> dict:
    user = await get_user(event_chat.id, dialog_manager=dialog_manager)
    async with APIClient() as client:
        teams = await client.get_teams_scoreboard()
    place = next(
        (place + 1 for place, team in enumerate(teams) if user.user_id in (user.id for user in team.users)), "∞"
    )
    return {"teams": teams, "place": place}
