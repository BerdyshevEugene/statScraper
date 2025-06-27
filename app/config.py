from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, SecretStr


class Settings(BaseSettings):
    login_url: HttpUrl
    username: str
    password: SecretStr
    headless: bool = False
    result_path: str = "./result/result.json"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="report_scraper_")


settings = Settings()
