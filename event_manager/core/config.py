import json
from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, ConstrainedStr, validator
from pydantic.networks import PostgresDsn


class LowerCaseString(ConstrainedStr):
    to_lower = True


class Settings(BaseSettings):
    PROJECT_NAME: str = "common_service"

    # Cross-domain request configuration
    BACKEND_CORS_ORIGINS: List = ["*"]

    # Database configuration
    POSTGRES_SERVER: str
    POSTGRES_PORT: Optional[str]
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT", 5432),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = {}
    SQLALCHEMY_SESSION_OPTIONS: Dict[str, Any] = {}

    @validator("SQLALCHEMY_ENGINE_OPTIONS", "SQLALCHEMY_SESSION_OPTIONS", pre=True)
    def convert_str_to_dict(cls, value: str):
        return json.loads(value) if isinstance(value, str) else value

    CURRENCY_API_KEY: str
    CURRENCY_API_KEY_1: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
