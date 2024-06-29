from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URI: str
    # STRIPE_API_KEY: str
    POSTGRES_DISABLE_JIT: bool = True
    POSTGRES_APPLICATION_NAME: str = "EventManager"
    POSTGRES_POOL_SIZE: int = 10
    POSTGRES_POOL_MAX_OVERFLOW: int = 20
    GOOGLE_MAPS_API_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
