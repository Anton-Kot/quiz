from datetime import timedelta
from typing import Any, AsyncGenerator
from uuid import UUID

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.sqlalchemy.repositories.quiz import QuizRepositorySqlAlchemy
from src.application.domain.exceptions import DuplicateItem, ItemNotFound
from src.adapters.sqlalchemy.models import QuizModel, SubjectModel
from src.application.domain.quiz import ChoiceAnswer, ChoiceQuestion, Difficulty, Quiz, Subject
from tests.integration.sqlalchemy.connect import get_nested_test_session


@pytest_asyncio.fixture(scope="function", name="admin_repo")
async def admin_repo_f(
    session_with_default_dataset: AsyncSession,
) -> AsyncGenerator[QuizRepositorySqlAlchemy, Any]:
    yield QuizRepositorySqlAlchemy(session_with_default_dataset)


@pytest_asyncio.fixture(name="session_with_default_dataset", scope="function")
async def session_with_default_dataset_f():
    async with get_nested_test_session() as session:

        subject1 = SubjectModel(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="subject1",
            description="subject1",
        )
        subject2 = SubjectModel(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            name="subject2",
            description="subject2",
        )
        session.add_all([subject1, subject2])
        await session.flush()

        quiz1 = QuizModel(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="quiz1",
            description="quiz1",
            time=timedelta(minutes=1),
            difficulty=Difficulty.EASY,
            subject_id=subject1.id,
            questions=[
                {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "text": "question1",
                    "answers": [
                        {
                            "id": "00000000-0000-0000-0000-000000000001",
                            "text": "answer1",
                            "is_correct": True,
                        },
                        {
                            "id": "00000000-0000-0000-0000-000000000002",
                            "text": "answer2",
                            "is_correct": False,
                        },
                    ],
                },
                {
                    "id": "00000000-0000-0000-0000-000000000002",
                    "text": "question2",
                    "answers": [
                        {
                            "id": "00000000-0000-0000-0000-000000000003",
                            "text": "answer3",
                            "is_correct": True,
                        },
                        {
                            "id": "00000000-0000-0000-0000-000000000004",
                            "text": "answer4",
                            "is_correct": False,
                        },
                    ],
                },
            ],
        )
        session.add(quiz1)

        await session.commit()

        yield session


@pytest.mark.asyncio
async def test_add_one_success(
    admin_repo: QuizRepositorySqlAlchemy, session_with_default_dataset: AsyncSession
):
    new_quiz = Quiz(
        id=UUID("00000000-0000-0000-0000-000000000003"),
        name="quiz3",
        description="quiz3 description",
        _time=timedelta(minutes=10),
        difficulty=Difficulty.MEDIUM,
        subject=Subject(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="subject1",
            description="subject1",
        ),
        _questions=[
            ChoiceQuestion(
                id=UUID("00000000-0000-0000-0000-000000000005"),
                text="New question",
                _answers=[
                    ChoiceAnswer(
                        id=UUID("00000000-0000-0000-0000-000000000005"), text="New answer", is_correct=True
                    )
                ],
            )
        ],
    )

    quiz_id = await admin_repo.add_one(new_quiz)
    assert quiz_id == new_quiz.id

    persisted = await session_with_default_dataset.scalar(
        select(QuizModel).where(QuizModel.id == new_quiz.id)
    )
    assert persisted is not None
    assert persisted.id == new_quiz.id
    assert persisted.name == new_quiz.name
    assert persisted.description == new_quiz.description
    assert persisted.time == new_quiz.time
    assert persisted.difficulty == new_quiz.difficulty
    assert persisted.subject_id == new_quiz.subject.id
    assert persisted.questions[0]["id"] == "00000000-0000-0000-0000-000000000005"
    assert persisted.questions[0]["answers"][0]["id"] == "00000000-0000-0000-0000-000000000005"


@pytest.mark.asyncio
async def test_add_one_duplicate(admin_repo: QuizRepositorySqlAlchemy):
    new_quiz = Quiz(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="quiz3",
        description="quiz3 description",
        _time=timedelta(minutes=10),
        difficulty=Difficulty.MEDIUM,
        subject=Subject(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="subject1",
            description="subject1",
        ),
        _questions=[
            ChoiceQuestion(
                id=UUID("00000000-0000-0000-0000-000000000005"),
                text="New question",
                _answers=[
                    ChoiceAnswer(
                        id=UUID("00000000-0000-0000-0000-000000000005"), text="New answer", is_correct=True
                    )
                ],
            )
        ],
    )
    with pytest.raises(DuplicateItem):
        await admin_repo.add_one(new_quiz)


@pytest.mark.asyncio
async def test_add_one_not_found_foreign_key(admin_repo: QuizRepositorySqlAlchemy):
    new_quiz = Quiz(
        id=UUID("00000000-0000-0000-0000-000000000003"),
        name="quiz3",
        description="quiz3 description",
        _time=timedelta(minutes=10),
        difficulty=Difficulty.MEDIUM,
        subject=Subject(
            id=UUID("00000000-0000-0000-0000-000000000100"),
            name="subject1",
            description="subject1",
        ),
        _questions=[
            ChoiceQuestion(
                id=UUID("00000000-0000-0000-0000-000000000005"),
                text="New question",
                _answers=[
                    ChoiceAnswer(
                        id=UUID("00000000-0000-0000-0000-000000000005"), text="New answer", is_correct=True
                    )
                ],
            )
        ],
    )
    with pytest.raises(ItemNotFound):
        await admin_repo.add_one(new_quiz)


@pytest.mark.asyncio
async def test_get_all(admin_repo: QuizRepositorySqlAlchemy):
    quizzes = await admin_repo.get_all()
    quizzes_list = list(quizzes)
    assert len(quizzes_list) == 1
    assert quizzes_list[0].name == "quiz1"
    assert isinstance(quizzes_list[0], Quiz)


@pytest.mark.asyncio
async def test_update_one(admin_repo: QuizRepositorySqlAlchemy, session_with_default_dataset: AsyncSession):
    updated_quiz = Quiz(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="updated quiz1",
        description="updated description",
        _time=timedelta(minutes=5),
        difficulty=Difficulty.HARD,
        subject=Subject(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            name="subject2",
            description="subject2",
        ),
        _questions=[
            ChoiceQuestion(
                id=UUID("00000000-0000-0000-0000-000000000001"),
                text="Updated question1",
                _answers=[
                    ChoiceAnswer(
                        id=UUID("00000000-0000-0000-0000-000000000001"),
                        text="Updated answer1",
                        is_correct=True,
                    )
                ],
            )
        ],
    )

    quiz_id = await admin_repo.update_one(updated_quiz.id, updated_quiz)
    assert quiz_id == updated_quiz.id

    result = await session_with_default_dataset.scalar(
        select(QuizModel).where(QuizModel.id == updated_quiz.id)
    )
    assert result is not None
    assert result.name == updated_quiz.name
    assert result.description == updated_quiz.description


@pytest.mark.asyncio
async def test_update_one_not_found(admin_repo: QuizRepositorySqlAlchemy):
    updated_quiz = Quiz(
        id=UUID("00000000-0000-0000-0000-000000000100"),
        name="updated quiz1",
        description="updated description",
        _time=timedelta(minutes=5),
        difficulty=Difficulty.HARD,
        subject=Subject(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            name="subject2",
            description="subject2",
        ),
        _questions=[
            ChoiceQuestion(
                id=UUID("00000000-0000-0000-0000-000000000001"),
                text="Updated question1",
                _answers=[
                    ChoiceAnswer(
                        id=UUID("00000000-0000-0000-0000-000000000001"),
                        text="Updated answer1",
                        is_correct=True,
                    )
                ],
            )
        ],
    )
    with pytest.raises(ItemNotFound):
        await admin_repo.update_one(updated_quiz.id, updated_quiz)


@pytest.mark.asyncio
async def test_update_one_not_found_foreign_key(admin_repo: QuizRepositorySqlAlchemy):
    updated_quiz = Quiz(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="quiz3",
        description="quiz3 description",
        _time=timedelta(minutes=10),
        difficulty=Difficulty.MEDIUM,
        subject=Subject(
            id=UUID("00000000-0000-0000-0000-000000000100"),
            name="subject1",
            description="subject1",
        ),
        _questions=[
            ChoiceQuestion(
                id=UUID("00000000-0000-0000-0000-000000000005"),
                text="New question",
                _answers=[
                    ChoiceAnswer(
                        id=UUID("00000000-0000-0000-0000-000000000005"), text="New answer", is_correct=True
                    )
                ],
            )
        ],
    )
    with pytest.raises(ItemNotFound):
        await admin_repo.update_one(updated_quiz.id, updated_quiz)


@pytest.mark.asyncio
async def test_delete_one(admin_repo: QuizRepositorySqlAlchemy, session_with_default_dataset: AsyncSession):
    quiz_id = UUID("00000000-0000-0000-0000-000000000001")
    deleted_id = await admin_repo.delete_one(quiz_id)
    assert deleted_id == quiz_id

    result = await session_with_default_dataset.scalar(select(QuizModel).where(QuizModel.id == quiz_id))
    assert result is None


@pytest.mark.asyncio
async def test_delete_one_not_found(admin_repo: QuizRepositorySqlAlchemy):
    quiz_id = UUID("00000000-0000-0000-0000-000000000100")
    with pytest.raises(ItemNotFound):
        await admin_repo.delete_one(quiz_id)
