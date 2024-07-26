from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOT_")

    token: str
    api_url: str
    api_username: str
    api_password: str

    parse_mode: str = "MarkdownV2"

    support_channel: int | None = None

    @property
    def bot(self) -> Bot:
        return Bot(
            token=self.token,
            default=DefaultBotProperties(parse_mode=self.parse_mode),
        )


bot = BotConfig()
