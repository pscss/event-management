from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str
    # STRIPE_API_KEY: str
    POSTGRES_APPLICATION_NAME: str = "Event Manager"
    POSTGRES_POOL_SIZE: int = 10
    POSTGRES_POOL_MAX_OVERFLOW: int = 20
    GOOGLE_MAPS_API_KEY: str
    TEST_DATABASE_URL: str
    TEST_SYNC_DATABASE_URL: str
    KEYCLOAK_VERSION: str
    KEYCLOAK_ADMIN: str
    KEYCLOAK_ADMIN_PASSWORD: str
    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str

    model_config = ConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
