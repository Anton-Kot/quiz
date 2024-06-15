from typing import Any

from src.application.domain.exceptions import DuplicateItem, ItemDataConflict, ItemNotFound, ReferencedItem


async def sqlalchemy_asyncpg_exception_mapper(exc: Exception):
    # Если делать для прода, лучше скрыть реальные названия столбцов и таблиц.

    if exc.orig.pgcode == "23505":  # == UniqueViolation
        raise DuplicateItem(
            detail=exc.orig.__cause__.detail, cause_entity=exc.orig.__cause__.table_name
        ) from exc

    # WARNING:  ASYNCPG FK ERR INCLUDES MORE THAN NOT FOUND ERRORS!!!
    if exc.orig.pgcode == "23503":  # == ForeignKeyViolationError

        if "DELETE" in exc.orig.__cause__.query:
            raise ReferencedItem(
                detail=exc.orig.__cause__.detail, cause_entity=exc.orig.__cause__.table_name
            ) from exc

        # if UPDATE, INSERT:
        raise ItemNotFound(
            detail=exc.orig.__cause__.detail,
            cause_entity=exc.orig.__cause__.detail.rsplit('in table "')[-1].rstrip('".'),
        ) from exc

    if exc.orig.pgcode == "23502":  # == NotNullViolationError
        raise ItemDataConflict(
            detail=f"Null value in field ({exc.orig.__cause__.column_name}) violates not-null constraint",
            cause_entity=exc.orig.__cause__.table_name,
        ) from exc

    raise exc


async def raise_item_not_found(key_name: str, key_value: Any, cause_entity: str):
    raise ItemNotFound(detail=f"Key ({key_name})=({key_value}) not found.", cause_entity=cause_entity)


async def raise_item_data_conflict(detail):
    raise ItemDataConflict(detail=detail)
