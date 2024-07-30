from aiogram import Dispatcher

from config.redis import redis

storage = redis.storage
dp = Dispatcher(storage=storage)
