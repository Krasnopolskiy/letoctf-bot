from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import html_decoration as hd
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from config.bot import bot
from dialogs.user.support.channels import SupportChannel


async def get_support_channels(**kwargs):
    return {"channels": list(SupportChannel)}


async def submit(message: Message, _: MessageInput, dialog_manager: DialogManager):
    text = "@{username} [{tg_id}]\n\n{text}\n\n#{channel}".format(
        username=message.from_user.username,
        tg_id=message.from_user.id,
        text=hd.bold(message.text),
        channel=dialog_manager.dialog_data["channel"],
    )
    if bot.support_channel is None:
        await message.reply("❌ Не задан канал поддержки")
        return
    await bot.bot.send_message(bot.support_channel, text)
    await message.reply("✅ Запрос отправлен")
    await dialog_manager.done()


async def set_channel(_: CallbackQuery, __: Any, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["channel"] = item_id


async def set_default_channel(_: Any, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.dialog().find("channel").set_checked(dialog_manager.event, "OTHER", dialog_manager)
