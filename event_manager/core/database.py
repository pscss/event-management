import json
from typing import Any, AsyncGenerator, Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import Pool

from event_manager.core.config import settings


def get_server_settings() -> dict[str, str] | None:
    server_settings: dict[str, str] = {}
    if settings.POSTGRES_DISABLE_JIT:
        server_settings["jit"] = "off"
    if settings.POSTGRES_APPLICATION_NAME:
        server_settings["application_name"] = settings.POSTGRES_APPLICATION_NAME
    return server_settings or None


def dumps(d: Any) -> str:
    return json.dumps(d, default=jsonable_encoder)


def create_engine(dsn: str, poolclass: Type[Pool] | None = None) -> AsyncEngine:
    kwargs: dict[str, Any] = {
        "pool_size": settings.POSTGRES_POOL_SIZE,
        "max_overflow": settings.POSTGRES_POOL_MAX_OVERFLOW,
    }

    if "asyncpg" in dsn.lower():
        server_settings = get_server_settings()
        if server_settings:
            kwargs["connect_args"] = {"server_settings": server_settings}

    return create_async_engine(dsn, **kwargs, json_serializer=dumps)


def get_engine() -> AsyncEngine:
    return create_engine(settings.DATABASE_URL)


def create_sessionmaker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


sessionmaker_instance = create_sessionmaker(get_engine())


async def with_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker_instance() as session:
        yield session
