from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str
    POSTGRES_APPLICATION_NAME: str = "Event Manager"
    POSTGRES_POOL_SIZE: int = 10
    POSTGRES_POOL_MAX_OVERFLOW: int = 20
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST_PORT: int = 5433
    DB_PORT: int = 5432

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
    KEYCLOAK_USERNAME: str
    # Keycloak DB
    KC_DB: str
    KC_DB_URL_HOST: str
    KC_DB_PASSWORD: str
    KC_DB_USERNAME: str
    KC_DB_SCHEMA: str

    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    SSL_KEY_FILE: str
    SSL_CERT_FILE: str

    model_config = ConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
