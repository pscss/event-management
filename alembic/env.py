from logging import getLogger
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from alembic import context
from event_manager import models
from event_manager.core.config import settings

logger = getLogger(__name__)
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = models.Base.metadata


def run_migrations_offline(url) -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(engine) -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    if not database_exists(engine.url):
        logger.info(f"Creating new database '{engine.url.database}'")
        create_database(engine.url)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


url = settings.SQLALCHEMY_DATABASE_URI
engine = create_engine(url)  # type:ignore
if context.is_offline_mode():
    run_migrations_offline(engine.url)
else:
    run_migrations_online(engine)
