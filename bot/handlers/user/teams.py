from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from api.client import APIClient
from api.structs import JoinTeamRequest
from handlers.auth import get_user


async def join_team_request(message: Message, dialog_manager: DialogManager) -> JoinTeamRequest:
    user = await get_user(message.chat.id, dialog_manager=dialog_manager)
    return JoinTeamRequest(
        user=user.user_id,
        invite=message.text,
    )


async def join(message: Message, _: MessageInput, dialog_manager: DialogManager):
    request = await join_team_request(message, dialog_manager)
    async with APIClient() as client:
        correct = await client.join_team(request)
    if correct:
        await message.reply("✅ Токен авторизован")
    else:
        await message.reply("❌ Токен не авторизован")
    await dialog_manager.done()
