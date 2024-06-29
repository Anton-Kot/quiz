
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import POSTGRE_DB_NAME, POSTGRE_HOST, POSTGRE_PASSWORD, POSTGRE_PORT, POSTGRE_USERNAME


DATABASE_URL = f"postgresql+asyncpg://{POSTGRE_USERNAME}:{POSTGRE_PASSWORD}@" \
               f"{POSTGRE_HOST}:{POSTGRE_PORT}/{POSTGRE_DB_NAME}"


engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession
)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata
