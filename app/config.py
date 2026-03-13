from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "stock_news"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    # API Keys
    finnhub_api_key: str = ""
    
    # Application
    app_name: str = "stock-news-api"
    app_debug: bool = True
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"
    
    @property
    def celery_broker_url(self) -> str:
        return self.redis_url
    
    @property
    def celery_result_backend(self) -> str:
        return self.redis_url
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
