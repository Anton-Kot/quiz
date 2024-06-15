from contextlib import AbstractAsyncContextManager
from typing import Protocol

from src.application.ports.quiz_admin_repo import AdminRepository


class UnitOfWork(AbstractAsyncContextManager, Protocol):
    """
    UoW, подвязанный на алхимию и то, что Data Access Layer будет
    иметь механизмы отслеживания изменений объектов, что не совсем
    его задача. Ужимает интерфейс Session и UnitOfWork и не является ни тем, ни другим.
    В идеале хочет видеть register-new, -delete, -dirty методы.
    Но такая реализация всё равно даёт плюсы: слабую связанность и тестируемость.
    Из минусов: нарушенный ISP и следовательно менее гибкое использование в будущем.
    Например, тяжело сделать вложенные транзакции, изоляцию с этим интерфейсом.
    """
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await super().__aexit__(exc_type, exc_value, traceback)
        await self.rollback()
        return None

    async def commit(self): ...

    async def rollback(self): ...


class AdminUnitOfWork(UnitOfWork):
    repo: AdminRepository

    def __init__(self, repo: AdminRepository):
        self.repo = repo
