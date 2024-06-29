from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Cross-domain request configuration
    BACKEND_CORS_ORIGINS: List = ["*"]

    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )
    # STRIPE_API_KEY: str
    POSTGRES_DISABLE_JIT: bool = True
    POSTGRES_APPLICATION_NAME: str = "EventManager"
    POSTGRES_POOL_SIZE: int = 10
    POSTGRES_POOL_MAX_OVERFLOW: int = 20


settings = Settings()
