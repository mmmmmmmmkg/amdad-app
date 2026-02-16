from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    database_url: str = "sqlite:///./amdad.db"
    timezone: str = "Africa/Cairo"

    scheduler_interval_seconds: int = Field(default=60, ge=10, le=3600)
    publish_retry_attempts: int = Field(default=3, ge=1, le=10)

    fb_page_id: str = ""
    fb_page_access_token: str = ""
    fb_graph_version: str = "v20.0"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
