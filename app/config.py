import sys

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, SecretStr


BASE_DIR = Path(__file__).resolve().parent.parent

if getattr(sys, "frozen", False):
    env_path = Path(sys.executable).parent / ".env"
else:
    env_path = BASE_DIR / ".env"


class Settings(BaseSettings):
    city: str
    headless: bool = False
    login_url: HttpUrl
    password: SecretStr
    queue_name: str
    result_path: str = "./result/result.json"
    rabbitmq_url: str
    username: str

    model_config = SettingsConfigDict(env_file=str(env_path), env_prefix="statScraper")


settings = Settings()
