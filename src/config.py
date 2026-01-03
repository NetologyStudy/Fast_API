from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()