import pytest_asyncio
from tests.integration.sqlalchemy.connect import create_database


@pytest_asyncio.fixture(autouse=True)
async def create_test_database(alembic_runner, alembic_engine):
    print("Creating test database...")
    await create_database()
    yield
    alembic_runner.migrate_down_to("base", return_current=False)
    print("Test database dropped.")
