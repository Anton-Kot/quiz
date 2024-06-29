from sanic import Request, Sanic
from sanic_ext import Extend
from sqlalchemy.ext.asyncio import AsyncSession
from src.adapters.sqlalchemy.repositories.quiz import QuizRepositorySqlAlchemy
from src.adapters.sqlalchemy.repositories.subject import SubjectRepositorySqlAlchemy
from src.application.ports.quiz import QuizRepository
from src.application.ports.subject import SubjectRepository
from src.adapters.sqlalchemy.uow import SqlAlchemyUnitOfWork
from src.application.ports.uow import UnitOfWork
from src.application.quiz_admin import SubjectAdminService
from src.adapters.sqlalchemy.connect import async_session_maker


def add_dependencies(app: Sanic):
    ext: Extend = app.ext

    ext.add_dependency(SubjectAdminService)
    ext.add_dependency(UnitOfWork, SqlAlchemyUnitOfWork)

    def supply_deduplicated_session(request: Request) -> AsyncSession:
        """Opened issue for cached dependencies ¯\\_(ツ)_/¯."""
        ctx = request.ctx
        if hasattr(ctx, "session"):
            return ctx.session
        ctx.session = async_session_maker()
        return ctx.session
    ext.add_dependency(AsyncSession, supply_deduplicated_session)

    ext.add_dependency(QuizRepository, QuizRepositorySqlAlchemy)
    ext.add_dependency(SubjectRepository, SubjectRepositorySqlAlchemy)
