from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.adapters.sqlalchemy.mappers import QuizSQLAlchemyMapper
from src.adapters.sqlalchemy.repositories.quiz_admin_repo import AdminRepositorySqlAlchemy
from src.application.domain.quiz import Quiz
from src.adapters.sqlalchemy.models import QuizModel


class QuizRepositorySqlAlchemy:
    def __init__(self, session: AsyncSession):
        self.admin_repo = AdminRepositorySqlAlchemy(
            model=QuizModel,
            model_key_field=QuizModel.id,
            session=session,
            dict_mapper=QuizSQLAlchemyMapper()
        )
        self.session = session
        self.model = QuizModel
        self.dict_mapper = QuizSQLAlchemyMapper()

    async def add_one(self, quiz: Quiz) -> UUID:
        return await self.admin_repo.add_one(quiz)

    async def get_all(self) -> list[Quiz]:
        quizzes = await self.session.scalars(select(self.model).options(joinedload(self.model.subject)))
        return (self.dict_mapper.model_to_domain(quiz) for quiz in quizzes)

    async def update_one(self, quiz_id: UUID, new_quiz: Quiz) -> UUID:
        return await self.admin_repo.update_one(quiz_id, new_quiz)

    async def delete_one(self, quiz_id: UUID) -> UUID:
        return await self.admin_repo.delete_one(quiz_id)
