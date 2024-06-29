
import asyncio
import pytest
from pytest_alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine
from tests.config import (
    TEST_POSTGRE_DB_NAME,
    TEST_POSTGRE_HOST,
    TEST_POSTGRE_PASSWORD,
    TEST_POSTGRE_PORT,
    TEST_POSTGRE_USERNAME,
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", name="db_url")
def db_url_fixture() -> str:
    url = (
        f"postgresql+asyncpg://{TEST_POSTGRE_USERNAME}:{TEST_POSTGRE_PASSWORD}@"
        f"{TEST_POSTGRE_HOST}:{TEST_POSTGRE_PORT}/{TEST_POSTGRE_DB_NAME}"
    )
    return url


@pytest.fixture()
def alembic_config():
    """Override this fixture to configure the exact alembic context setup required."""
    return Config()


@pytest.fixture
def alembic_engine(db_url):
    """Override this fixture to provide pytest-alembic powered tests with a database handle."""
    return create_async_engine(db_url, echo=True)
