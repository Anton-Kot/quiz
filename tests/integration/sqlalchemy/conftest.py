
import pytest_asyncio
from tests.integration.sqlalchemy.connect import create_database, drop_models, init_models


@pytest_asyncio.fixture(scope="module", autouse=True)
async def create_test_database():
    print("Creating test database...")
    await create_database()
    await init_models()
    yield
    await drop_models()
    print("Test database dropped.")
