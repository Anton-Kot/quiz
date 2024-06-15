from unittest.mock import AsyncMock
from uuid import UUID, uuid4
from datetime import timedelta
import pytest

from src.application.ports.uow import AdminUnitOfWork
from src.application.domain.quiz import ChoiceAnswer, ChoiceQuestion, Quiz, Subject
from src.application.quiz_admin import (
    SubjectDTO,
    QuizAdminDTO,
    ChoiceQuestionAdminDTO,
    ChoiceAnswerAdminDTO,
    SubjectAdminService,
    QuizAdminService,
)


class FakeUoW(AdminUnitOfWork):
    commited = False

    async def commit(self):
        self.commited = True

    async def rollback(self): ...


@pytest.fixture(name="mock_uow")
def mock_uow_f():
    uow = FakeUoW(repo=AsyncMock())
    return uow


@pytest.fixture(name="subject_admin_service")
def subject_admin_service_f(mock_uow):
    return SubjectAdminService(uow=mock_uow)


@pytest.fixture(name="quiz_admin_service")
def quiz_admin_service_f(mock_uow):
    return QuizAdminService(uow=mock_uow)


@pytest.mark.asyncio
async def test_create_one_subject(subject_admin_service):
    # Test data
    dto = SubjectDTO(name="History", description="History Subject")
    mock_uow = subject_admin_service.uow
    mock_uow.repo.add_one.return_value = uuid4()

    # Test create_one
    created_id = await subject_admin_service.create_one(dto)
    assert mock_uow.repo.add_one.called
    assert mock_uow.commited
    assert isinstance(created_id, UUID)


@pytest.mark.asyncio
async def test_get_all_subjects(subject_admin_service):
    # Test data
    subject_id = uuid4()
    domain_object = Subject(id=subject_id, name="Geography", description="Geography Subject")
    mock_uow = subject_admin_service.uow
    mock_uow.repo.get_all.return_value = [domain_object]

    # Test get_all
    result = await subject_admin_service.get_all()
    assert len(result) == 1
    assert result[0].id == subject_id
    assert result[0].name == "Geography"
    assert result[0].description == "Geography Subject"


@pytest.mark.asyncio
async def test_update_one_subject(subject_admin_service):
    # Test data
    subject_id = uuid4()
    dto = SubjectDTO(name="Updated History", description="Updated History Subject")
    mock_uow = subject_admin_service.uow
    mock_uow.repo.update_one.return_value = subject_id

    # Test update_one
    updated_id = await subject_admin_service.update_one(subject_id, dto)
    assert mock_uow.repo.update_one.called
    assert mock_uow.commited
    assert updated_id == subject_id


@pytest.mark.asyncio
async def test_delete_one_subject(subject_admin_service):
    # Test data
    subject_id = uuid4()
    mock_uow = subject_admin_service.uow
    mock_uow.repo.delete_one.return_value = subject_id

    # Test delete_one
    deleted_id = await subject_admin_service.delete_one(subject_id)
    assert mock_uow.repo.delete_one.called
    assert mock_uow.commited
    assert deleted_id == subject_id


@pytest.mark.asyncio
async def test_create_one_quiz(quiz_admin_service):
    # Test data
    subject = Subject(id=uuid4(), name="Science", description="Science Subject")
    answer_edit_dto = ChoiceAnswerAdminDTO(is_correct=True, text="Correct Answer")
    question_edit_dto = ChoiceQuestionAdminDTO(text="Sample Question", answers=[answer_edit_dto])
    dto = QuizAdminDTO(
        name="Sample Quiz",
        description="This is a sample quiz",
        time=timedelta(minutes=30),
        difficulty="Easy",
        subject=subject,
        questions=[question_edit_dto],
    )
    mock_uow = quiz_admin_service.uow
    mock_uow.repo.add_one.return_value = uuid4()

    # Test create_one
    created_id = await quiz_admin_service.create_one(dto)
    assert mock_uow.repo.add_one.called
    assert mock_uow.commited
    assert isinstance(created_id, UUID)


@pytest.mark.asyncio
async def test_get_all_quizzes(quiz_admin_service):
    # Test data
    subject = Subject(id=uuid4(), name="Science", description="Science Subject")
    answer = ChoiceAnswer(id=uuid4(), is_correct=True, text="Correct Answer")
    question = ChoiceQuestion(id=uuid4(), text="Sample Question", _answers=[answer])
    quiz_id = uuid4()
    domain_object = Quiz(
        id=quiz_id,
        name="Sample Quiz",
        description="This is a sample quiz",
        _time=timedelta(minutes=30),
        difficulty="Easy",
        subject=subject,
        _questions=[question],
    )
    mock_uow = quiz_admin_service.uow
    mock_uow.repo.get_all.return_value = [domain_object]

    # Test get_all
    result = await quiz_admin_service.get_all()
    assert len(result) == 1
    assert result[0].id == quiz_id
    assert result[0].name == "Sample Quiz"
    assert result[0].description == "This is a sample quiz"


@pytest.mark.asyncio
async def test_update_one_quiz(quiz_admin_service):
    # Test data
    quiz_id = uuid4()
    subject = Subject(id=uuid4(), name="Science", description="Science Subject")
    answer_edit_dto = ChoiceAnswerAdminDTO(is_correct=True, text="Correct Answer")
    question_edit_dto = ChoiceQuestionAdminDTO(text="Sample Question", answers=[answer_edit_dto])
    dto = QuizAdminDTO(
        name="Updated Quiz",
        description="This is an updated quiz",
        time=timedelta(minutes=45),
        difficulty="Medium",
        subject=subject,
        questions=[question_edit_dto],
    )
    mock_uow = quiz_admin_service.uow
    mock_uow.repo.update_one.return_value = quiz_id

    # Test update_one
    updated_id = await quiz_admin_service.update_one(quiz_id, dto)
    assert mock_uow.repo.update_one.called
    assert mock_uow.commited
    assert updated_id == quiz_id


@pytest.mark.asyncio
async def test_delete_one_quiz(quiz_admin_service):
    # Test data
    quiz_id = uuid4()
    mock_uow = quiz_admin_service.uow
    mock_uow.repo.delete_one.return_value = quiz_id

    # Test delete_one
    deleted_id = await quiz_admin_service.delete_one(quiz_id)
    assert mock_uow.repo.delete_one.called
    assert mock_uow.commited
    assert deleted_id == quiz_id
