from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from src.adapters.sqlalchemy.mappers import SQLAlchemyMapper
from src.adapters.sqlalchemy.connect import Base
from src.adapters.sqlalchemy.exc_mappers import raise_item_not_found, sqlalchemy_asyncpg_exception_mapper


class AdminRepositorySqlAlchemy:
    model: Base
    model_key_field: InstrumentedAttribute
    session: AsyncSession
    dict_mapper: SQLAlchemyMapper

    def __init__(self, model, model_key_field, session, dict_mapper) -> None:
        self.model = model
        self.model_key_field = model_key_field
        self.session = session
        self.dict_mapper = dict_mapper

    async def add_one(self, domain_object):
        try:
            row_id = await self.session.scalar(
                insert(self.model).returning(self.model_key_field),
                self.dict_mapper.domain_to_dict(domain_object),
            )
            return str(row_id)

        except IntegrityError as e:
            await sqlalchemy_asyncpg_exception_mapper(e)

    async def get_all(self):
        quizzes = await self.session.scalars(select(self.model))
        return (self.dict_mapper.model_to_domain(quiz) for quiz in quizzes)

    async def update_one(self, key, updated_domain_object):
        try:
            row_id = await self.session.scalar(
                update(self.model)
                .returning(self.model_key_field)
                .where(self.model_key_field == key)
                .values(self.dict_mapper.domain_to_dict(updated_domain_object))
            )
            if row_id is None:
                await raise_item_not_found(self.model_key_field, key, self.model.__name__)
            return row_id

        except IntegrityError as e:
            await sqlalchemy_asyncpg_exception_mapper(e)

    async def delete_one(self, object_id):
        try:
            row_id = await self.session.scalar(
                delete(self.model).returning(self.model_key_field).where(self.model_key_field == object_id)
            )
            if row_id is None:
                await raise_item_not_found(self.model_key_field, object_id, self.model.__name__)
            return row_id

        except IntegrityError as e:
            await sqlalchemy_asyncpg_exception_mapper(e)
