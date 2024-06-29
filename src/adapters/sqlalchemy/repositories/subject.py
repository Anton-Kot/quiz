from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.adapters.sqlalchemy.mappers import SubjectSQLAlchemyMapper
from src.adapters.sqlalchemy.repositories.quiz_admin_repo import AdminRepositorySqlAlchemy
from src.application.domain.quiz import Subject
from src.adapters.sqlalchemy.models import SubjectModel


class SubjectRepositorySqlAlchemy:
    def __init__(self, session: AsyncSession):
        self.admin_repo = AdminRepositorySqlAlchemy(
            model=SubjectModel,
            model_key_field=SubjectModel.id,
            session=session,
            dict_mapper=SubjectSQLAlchemyMapper()
        )
        self.session = session
        self.model = SubjectModel
        self.dict_mapper = SubjectSQLAlchemyMapper()

    async def add_one(self, subject: Subject) -> UUID:
        return await self.admin_repo.add_one(subject)

    async def get_all(self) -> list[Subject]:
        return await self.admin_repo.get_all()

    async def update_one(self, subject_id: UUID, new_subject: Subject) -> UUID:
        return await self.admin_repo.update_one(subject_id, new_subject)

    async def delete_one(self, subject_id: UUID) -> UUID:
        return await self.admin_repo.delete_one(subject_id)
