
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from alembic.command import downgrade, upgrade
from alembic.config import Config

from tests.config import (
    TEST_POSTGRE_DB_NAME,
    TEST_POSTGRE_HOST,
    TEST_POSTGRE_PASSWORD,
    TEST_POSTGRE_PORT,
    TEST_POSTGRE_USERNAME,
)


DATABASE_URL = (
    f"postgresql+asyncpg://{TEST_POSTGRE_USERNAME}:{TEST_POSTGRE_PASSWORD}@"
    f"{TEST_POSTGRE_HOST}:{TEST_POSTGRE_PORT}/{TEST_POSTGRE_DB_NAME}"
)


engine = create_async_engine(DATABASE_URL, echo=True)

async_sessionmaker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)  # expire_on_commit: не хотим новые запросы для уже закоммиченных объектов


async def init_models(real_alembic_config: Config):
    upgrade(real_alembic_config, "head")


async def drop_models(real_alembic_config: Config):
    downgrade(real_alembic_config, "base")


async def create_database():
    conn = await asyncpg.connect(
        host=TEST_POSTGRE_HOST,
        port=TEST_POSTGRE_PORT,
        user=TEST_POSTGRE_USERNAME,
        password=TEST_POSTGRE_PASSWORD,
        database="postgres",
    )
    try:
        await conn.execute(f"CREATE DATABASE {TEST_POSTGRE_DB_NAME}")  # :c
    except asyncpg.DuplicateDatabaseError:
        print("Database already exists")
    finally:
        await conn.close()


@asynccontextmanager
async def get_nested_test_session() -> AsyncGenerator[AsyncSession, Any]:
    """
    Session-as-a-Nested transaction for tests

    Auto rollbacks all changes in the session.
    """
    async with engine.connect() as conn:

        async with conn.begin() as transaction:  # Enclosing transaction

            async with AsyncSession(
                bind=conn, join_transaction_mode="create_savepoint", expire_on_commit=False
            ) as async_session:

                print(f"Start nested transaction: {async_session}")
                yield async_session

            print("Close nested transaction.")
            await transaction.rollback()
            print("Rollback enclosing transaction.")
        print("Close enclosing transaction.")
    print("Connection close.")
