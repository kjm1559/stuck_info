from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "FastAPI Async App"
    app_debug: bool = True
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
