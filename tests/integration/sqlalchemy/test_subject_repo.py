from typing import Any, AsyncGenerator
from uuid import UUID

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.sqlalchemy.repositories.subject import SubjectRepositorySqlAlchemy
from src.application.domain.exceptions import DuplicateItem, ItemNotFound
from src.adapters.sqlalchemy.models import SubjectModel
from src.application.domain.quiz import Subject
from tests.integration.sqlalchemy.connect import get_nested_test_session


@pytest_asyncio.fixture(scope="function", name="admin_repo")
async def admin_repo_f(
    session_with_default_dataset: AsyncSession,
) -> AsyncGenerator[SubjectRepositorySqlAlchemy, Any]:
    yield SubjectRepositorySqlAlchemy(session_with_default_dataset)


@pytest_asyncio.fixture(name="session_with_default_dataset", scope="function")
async def session_with_default_dataset_f():
    async with get_nested_test_session() as session:
        subject1 = SubjectModel(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="subject1",
            description="subject1 description",
        )
        subject2 = SubjectModel(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            name="subject2",
            description="subject2 description",
        )
        session.add_all([subject1, subject2])
        await session.commit()

        yield session


@pytest.mark.asyncio
async def test_add_one_success(
    admin_repo: SubjectRepositorySqlAlchemy, session_with_default_dataset: AsyncSession
):
    new_subject = Subject(
        id=UUID("00000000-0000-0000-0000-000000000003"),
        name="subject3",
        description="subject3 description",
    )

    subject_id = await admin_repo.add_one(new_subject)
    assert subject_id == new_subject.id

    persisted = await session_with_default_dataset.scalar(
        select(SubjectModel).where(SubjectModel.id == new_subject.id)
    )
    assert persisted is not None
    assert persisted.id == new_subject.id
    assert persisted.name == new_subject.name
    assert persisted.description == new_subject.description


@pytest.mark.asyncio
async def test_add_one_duplicate(admin_repo: SubjectRepositorySqlAlchemy):
    duplicate_subject = Subject(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="duplicate subject",
        description="duplicate subject description",
    )
    with pytest.raises(DuplicateItem):
        await admin_repo.add_one(duplicate_subject)


@pytest.mark.asyncio
async def test_get_all(admin_repo: SubjectRepositorySqlAlchemy):
    subjects = await admin_repo.get_all()
    subjects_list = list(subjects)
    assert len(subjects_list) == 2
    assert subjects_list[0].name in ["subject1", "subject2"]
    assert isinstance(subjects_list[0], Subject)


@pytest.mark.asyncio
async def test_update_one(
    admin_repo: SubjectRepositorySqlAlchemy, session_with_default_dataset: AsyncSession
):
    updated_subject = Subject(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="updated subject1",
        description="updated description",
    )

    subject_id = await admin_repo.update_one(updated_subject.id, updated_subject)
    assert subject_id == updated_subject.id

    result = await session_with_default_dataset.scalar(
        select(SubjectModel).where(SubjectModel.id == updated_subject.id)
    )
    assert result is not None
    assert result.name == updated_subject.name
    assert result.description == updated_subject.description


@pytest.mark.asyncio
async def test_update_one_not_found(admin_repo: SubjectRepositorySqlAlchemy):
    non_existent_subject = Subject(
        id=UUID("00000000-0000-0000-0000-000000000100"),
        name="non-existent subject",
        description="non-existent subject description",
    )
    with pytest.raises(ItemNotFound):
        await admin_repo.update_one(non_existent_subject.id, non_existent_subject)


@pytest.mark.asyncio
async def test_delete_one(
    admin_repo: SubjectRepositorySqlAlchemy, session_with_default_dataset: AsyncSession
):
    subject_id = UUID("00000000-0000-0000-0000-000000000001")
    deleted_id = await admin_repo.delete_one(subject_id)
    assert deleted_id == subject_id

    result = await session_with_default_dataset.scalar(
        select(SubjectModel).where(SubjectModel.id == subject_id)
    )
    assert result is None


@pytest.mark.asyncio
async def test_delete_one_not_found(admin_repo: SubjectRepositorySqlAlchemy):
    non_existent_id = UUID("00000000-0000-0000-0000-000000000100")
    with pytest.raises(ItemNotFound):
        await admin_repo.delete_one(non_existent_id)
