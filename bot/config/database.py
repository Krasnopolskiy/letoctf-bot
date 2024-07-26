from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MYSQL_")

    host: str
    port: str
    database: str
    user: str
    password: str

    template: str = "mysql://{user}:{password}@{host}:{port}/{database}"

    @property
    def url(self) -> str:
        return self.template.format(**self.model_dump())


db = DatabaseConfig()
