
from typing import Any, AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import POSTGRE_DB_NAME, POSTGRE_HOST, POSTGRE_PASSWORD, POSTGRE_PORT, POSTGRE_USERNAME


DATABASE_URL = f"postgresql+asyncpg://{POSTGRE_USERNAME}:{POSTGRE_PASSWORD}@" \
               f"{POSTGRE_HOST}:{POSTGRE_PORT}/{POSTGRE_DB_NAME}"


engine = create_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass


def init_models():
    Base.metadata.create_all(engine)
