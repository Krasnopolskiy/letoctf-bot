from aiogram.types import Message

from database.queries import find_user_by_tg_id


async def authenticated(message: Message) -> bool:
    user = find_user_by_tg_id(message.from_user.id)
    return user is not None


async def unauthenticated(message: Message) -> bool:
    user = find_user_by_tg_id(message.from_user.id)
    return user is None
