import json

from aiogram.types import CallbackQuery, Chat, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, ManagedCheckbox, Select
from api.client import APIClient
from api.structs import Challenge, SubmitChallengeRequest
from config.s3 import s3
from dialogs.user.challenges.states import UserChallengesStateGroup
from handlers.auth import get_user


def submit_request(message: Message, user_id: int) -> SubmitChallengeRequest:
    return SubmitChallengeRequest(
        user=user_id,
        flag=message.text,
    )


def is_not_solved(data: dict, _: Whenable, __: DialogManager):
    selected = json.loads(data["dialog_data"]["selected"])
    challenge = Challenge(**selected)
    return not challenge.solved


def has_assets(data: dict, _: Whenable, __: DialogManager) -> bool:
    challenge = Challenge(**data)
    return len(challenge.files) > 0


def filter_solved_challenges(dialog_manager: DialogManager, challenges: list[Challenge]) -> list[Challenge]:
    show_solved = dialog_manager.dialog_data.get("show_solved", True)
    if not show_solved:
        challenges = filter(lambda challenge: not challenge.solved, challenges)
    return list(challenges)


async def list_challenges(event_chat: Chat, dialog_manager: DialogManager, **kwargs) -> dict[str, list[Challenge]]:
    user = await get_user(event_chat.id, dialog_manager=dialog_manager)
    async with APIClient() as client:
        challenges = await client.get_challenges(user.user_id)
    challenges = filter_solved_challenges(dialog_manager, challenges)
    return {"challenges": challenges}


async def select(callback: CallbackQuery, _: Select, dialog_manager: DialogManager, item_id: str):
    user = await get_user(callback.message.chat.id, dialog_manager=dialog_manager)
    async with APIClient() as client:
        challenge = await client.get_challenge(item_id, user.user_id)
    await dialog_manager.update({"selected": challenge.model_dump_json()})
    await dialog_manager.switch_to(UserChallengesStateGroup.render)


async def render(dialog_manager: DialogManager, **kwargs) -> dict:
    selected = json.loads(dialog_manager.dialog_data["selected"])
    return Challenge(**selected).model_dump()


async def toggle_solved(_: CallbackQuery, checkbox: ManagedCheckbox, dialog_manager: DialogManager):
    await dialog_manager.update({"show_solved": checkbox.is_checked()})
    await dialog_manager.switch_to(UserChallengesStateGroup.list)


async def submit(message: Message, _: MessageInput, dialog_manager: DialogManager):
    selected = json.loads(dialog_manager.dialog_data["selected"])
    challenge = Challenge(**selected)
    user = await get_user(message.chat.id, dialog_manager=dialog_manager)
    request = submit_request(message, user.user_id)

    async with APIClient() as client:
        correct = await client.submit_challenge(challenge.id, request)

    if correct:
        await message.reply("✅ Верный флаг")
    else:
        await message.reply("❌ Неверный флаг")

    await dialog_manager.switch_to(UserChallengesStateGroup.list)


async def submit_hidden(message: Message, _: MessageInput, dialog_manager: DialogManager):
    user = await get_user(message.chat.id, dialog_manager=dialog_manager)
    request = submit_request(message, user.user_id)

    async with APIClient() as client:
        correct = await client.submit_hidden_challenge(request)

    if correct:
        await message.reply("✅ Верный флаг")
    else:
        await message.reply("❌ Неверный флаг")

    await dialog_manager.switch_to(UserChallengesStateGroup.list)


async def send_assets(callback: CallbackQuery, _: Button, dialog_manager: DialogManager):
    selected = json.loads(dialog_manager.dialog_data["selected"])
    challenge = Challenge(**selected)
    documents = [s3.read_document(file.s3_key) for file in challenge.files]
    await callback.bot.send_media_group(chat_id=callback.message.chat.id, media=documents)
