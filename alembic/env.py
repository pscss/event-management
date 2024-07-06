import asyncio
from logging import getLogger
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy_utils import database_exists

from alembic import context
from event_manager import models
from event_manager.core.config import settings

logger = getLogger(__name__)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = models.Base.metadata


async def check_database_exists(connectable: AsyncEngine):
    """Check if the database exists."""
    try:
        logger.info("Checking if database exists...")
        async with connectable.connect() as connection:
            exists = await connection.run_sync(
                lambda conn: database_exists(conn.engine.url)
            )
            logger.info(f"Database exists: {exists}")
            return exists
    except Exception as e:
        logger.exception(f"Error checking database existence: {e}")
        return False


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    logger.info("Running migrations in offline mode...")
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        logger.info("Starting offline migration transaction...")
        context.run_migrations()
        logger.info("Offline migrations completed successfully.")


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    logger.info("Running migrations in online mode...")
    logger.info(f"Database URI: {settings.DATABASE_URL}")
    connectable = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    if not await check_database_exists(connectable):
        logger.info("Database does not exist. Exiting migration.")
        return
    try:
        async with connectable.connect() as connection:
            logger.info("Connected to the database.")
            await connection.run_sync(
                lambda conn: context.configure(
                    connection=conn, target_metadata=target_metadata
                )
            )
            logger.info("Configuration completed. Starting migrations...")
            await connection.run_sync(lambda _: context.run_migrations())
            await connection.commit()
            logger.info("Online migrations completed successfully.")
    except Exception as e:
        logger.exception(f"Error during migration: {e}")
        await connection.rollback()

    await connectable.dispose()
    logger.exception("Database connection disposed.")


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
