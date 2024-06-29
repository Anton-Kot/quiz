import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config

from alembic import context
import alembic_postgresql_enum  # pylint: disable=W0611  # noqa: F401

from src.adapters.sqlalchemy.connect import Base
from src.config import POSTGRE_DB_NAME, POSTGRE_HOST, POSTGRE_PASSWORD, POSTGRE_PORT, POSTGRE_USERNAME


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRE_USERNAME}:{POSTGRE_PASSWORD}@"
    f"{POSTGRE_HOST}:{POSTGRE_PORT}/{POSTGRE_DB_NAME}"
)
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations(connectable: AsyncEngine) -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    Changed for async/sync engines support for pytest-alembic.
    """
    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        connectable = async_engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )

    # Note, we decide whether to run asynchronously based on the kind of engine we're dealing with.
    if isinstance(connectable, AsyncEngine):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(run_async_migrations(connectable))
        else:
            loop.create_task(run_async_migrations(connectable))
    else:
        do_run_migrations(connectable)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
