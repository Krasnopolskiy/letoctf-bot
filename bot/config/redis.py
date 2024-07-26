from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio.client import Redis


class RedisConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    host: str
    port: int

    @property
    def redis(self) -> Redis:
        return Redis(host=self.host, port=self.port, decode_responses=True)

    @property
    def storage(self) -> RedisStorage:
        return RedisStorage(self.redis, key_builder=DefaultKeyBuilder(with_destiny=True))


redis = RedisConfig()
