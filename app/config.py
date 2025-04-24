import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    BASE_SITE: str
    INFOBASE_SITE : str
    ADMIN_ID: int
    YANDEX_MAPS_API_KEY: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

    def get_webhook_url(self) -> str:
        return f"{self.BASE_SITE}/webhook"


settings = Settings()