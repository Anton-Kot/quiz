from uuid import uuid4
from datetime import timedelta
import pytest

from src.application.quiz_admin import (
    ChoiceAnswerAdminDTO,
    ChoiceQuestionAdminDTO,
    QuizAdminDTO,
    SubjectDomainMapper,
    QuizDomainMapper,
    SubjectDTO,
)
from src.application.domain.quiz import Subject, Quiz, ChoiceQuestion, ChoiceAnswer


@pytest.fixture(name="subject_domain_mapper")
def subject_domain_mapper_f():
    return SubjectDomainMapper()


@pytest.fixture(name="quiz_domain_mapper")
def quiz_domain_mapper_f():
    return QuizDomainMapper()


def test_subject_domain_mapper(subject_domain_mapper):
    # Test data
    subject_edit_dto = SubjectDTO(name="Math", description="Mathematics Subject")
    subject = Subject(id=uuid4(), name="Math", description="Mathematics Subject")

    # Test map_dto_to_domain_object
    domain_object = subject_domain_mapper.map_dto_to_domain_object(subject_edit_dto)
    assert domain_object.name == subject_edit_dto.name
    assert domain_object.description == subject_edit_dto.description

    # Test map_domain_object_to_dto
    subject_read_dto = subject_domain_mapper.map_domain_object_to_dto(subject)
    assert subject_read_dto.id == subject.id
    assert subject_read_dto.name == subject.name
    assert subject_read_dto.description == subject.description


def test_quiz_domain_mapper(quiz_domain_mapper):
    # Test data
    subject = Subject(id=uuid4(), name="Science", description="Science Subject")
    answer_edit_dto = ChoiceAnswerAdminDTO(is_correct=True, text="Correct Answer")
    question_edit_dto = ChoiceQuestionAdminDTO(text="Sample Question", answers=[answer_edit_dto])
    quiz_edit_dto = QuizAdminDTO(
        name="Sample Quiz",
        description="This is a sample quiz",
        time=timedelta(minutes=30),
        difficulty="Easy",
        subject=subject,
        questions=[question_edit_dto],
    )

    answer = ChoiceAnswer(id=uuid4(), is_correct=True, text="Correct Answer")
    question = ChoiceQuestion(id=uuid4(), text="Sample Question", _answers=[answer])
    quiz = Quiz(
        id=uuid4(),
        name="Sample Quiz",
        description="This is a sample quiz",
        _time=timedelta(minutes=30),
        difficulty="Easy",
        subject=subject,
        _questions=[question],
    )

    # Test map_dto_to_domain_object
    domain_object = quiz_domain_mapper.map_dto_to_domain_object(quiz_edit_dto)
    assert domain_object.name == quiz_edit_dto.name
    assert domain_object.description == quiz_edit_dto.description
    assert domain_object.time == quiz_edit_dto.time
    assert domain_object.difficulty == quiz_edit_dto.difficulty
    assert domain_object.subject == quiz_edit_dto.subject
    assert len(domain_object.questions) == len(quiz_edit_dto.questions)
    assert domain_object.questions[0].text == quiz_edit_dto.questions[0].text
    assert domain_object.questions[0].answers[0].text == quiz_edit_dto.questions[0].answers[0].text

    # Test map_domain_object_to_dto
    quiz_read_dto = quiz_domain_mapper.map_domain_object_to_dto(quiz)
    assert quiz_read_dto.id == quiz.id
    assert quiz_read_dto.name == quiz.name
    assert quiz_read_dto.description == quiz.description
    assert quiz_read_dto.time == quiz.time
    assert quiz_read_dto.difficulty == quiz.difficulty
    assert quiz_read_dto.subject == quiz.subject
    assert len(quiz_read_dto.questions) == len(quiz.questions)
    assert quiz_read_dto.questions[0].id == quiz.questions[0].id
    assert quiz_read_dto.questions[0].text == quiz.questions[0].text
    assert quiz_read_dto.questions[0].answers[0].id == quiz.questions[0].answers[0].id
    assert quiz_read_dto.questions[0].answers[0].text == quiz.questions[0].answers[0].text
