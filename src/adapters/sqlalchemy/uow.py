
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.ports.uow import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def __aenter__(self):
        await self.async_session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.async_session.__aexit__(exc_type, exc_value, traceback)

    async def commit(self):
        await self.async_session.commit()

    async def rollback(self):
        await self.async_session.rollback()
