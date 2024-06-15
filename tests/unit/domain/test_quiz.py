from datetime import timedelta
from uuid import uuid4
import pytest
from src.application.domain.quiz import Quiz, ChoiceQuestion, ChoiceAnswer, Difficulty, Subject


@pytest.fixture(name="subject")
def subject_fixture():
    return Subject(
        id=uuid4(),
        name="subj",
        description="subject1",
    )


@pytest.fixture(name="valid_questions")
def valid_questions_fixture():
    return [
        ChoiceQuestion(
            id=uuid4(),
            text="Question 1",
            _answers=[ChoiceAnswer(id=uuid4(), text="Answer 1", is_correct=True)],
        )
    ]


def test_quiz_creation_with_valid_data(subject, valid_questions):
    quiz = Quiz(
        id=uuid4(),
        name="Sample Quiz",
        description="A sample quiz",
        _time=timedelta(minutes=30),
        difficulty=Difficulty.EASY,
        subject=subject,
        _questions=valid_questions,
    )
    assert quiz.questions == valid_questions


def test_quiz_creation_with_no_questions(subject):
    with pytest.raises(ValueError, match="Quiz must have between 1 and 100 questions"):
        Quiz(
            id=uuid4(),
            name="Sample Quiz",
            description="A sample quiz",
            _time=timedelta(minutes=30),
            difficulty=Difficulty.EASY,
            subject=subject,
            _questions=[],
        )


def test_quiz_creation_with_too_many_questions(subject):
    questions = [
        ChoiceQuestion(
            id=uuid4(),
            text=f"Question {i+1}",
            _answers=[ChoiceAnswer(id=uuid4(), text="Answer 1", is_correct=True)],
        )
        for i in range(101)
    ]
    with pytest.raises(ValueError, match="Quiz must have between 1 and 100 questions"):
        Quiz(
            id=uuid4(),
            name="Sample Quiz",
            description="A sample quiz",
            _time=timedelta(minutes=30),
            difficulty=Difficulty.EASY,
            subject=subject,
            _questions=questions,
        )


def test_quiz_creation_with_too_short_time(subject, valid_questions):
    with pytest.raises(ValueError, match="Quiz time must be between 0:01:00 and 4:00:00"):
        Quiz(
            id=uuid4(),
            name="Sample Quiz",
            description="A sample quiz",
            _time=timedelta(seconds=30),
            difficulty=Difficulty.EASY,
            subject=subject,
            _questions=valid_questions,
        )


def test_quiz_creation_with_too_long_time(subject, valid_questions):
    with pytest.raises(ValueError, match="Quiz time must be between 0:01:00 and 4:00:00"):
        Quiz(
            id=uuid4(),
            name="Sample Quiz",
            description="A sample quiz",
            _time=timedelta(minutes=300),
            difficulty=Difficulty.EASY,
            subject=subject,
            _questions=valid_questions,
        )


def test_quiz_set_valid_time(subject, valid_questions):
    quiz = Quiz(
        id=uuid4(),
        name="Sample Quiz",
        description="A sample quiz",
        _time=timedelta(minutes=30),
        difficulty=Difficulty.EASY,
        subject=subject,
        _questions=valid_questions,
    )

    new_time = timedelta(minutes=60)
    quiz.time = new_time
    assert quiz.time == new_time


def test_quiz_set_invalid_time(subject, valid_questions):
    quiz = Quiz(
        id=uuid4(),
        name="Sample Quiz",
        description="A sample quiz",
        _time=timedelta(minutes=30),
        difficulty=Difficulty.EASY,
        subject=subject,
        _questions=valid_questions,
    )

    with pytest.raises(ValueError, match="Quiz time must be between 0:01:00 and 4:00:00"):
        quiz.time = timedelta(seconds=30)


def test_quiz_set_valid_questions(subject, valid_questions):
    quiz = Quiz(
        id=uuid4(),
        name="Sample Quiz",
        description="A sample quiz",
        _time=timedelta(minutes=30),
        difficulty=Difficulty.EASY,
        subject=subject,
        _questions=valid_questions,
    )

    new_questions = [
        ChoiceQuestion(
            id=uuid4(),
            text="Question 2",
            _answers=[ChoiceAnswer(id=uuid4(), text="Answer 2", is_correct=True)],
        ),
        ChoiceQuestion(
            id=uuid4(),
            text="Question 3",
            _answers=[ChoiceAnswer(id=uuid4(), text="Answer 3", is_correct=True)],
        ),
    ]
    quiz.questions = new_questions
    assert quiz.questions == new_questions


def test_quiz_set_invalid_questions(subject, valid_questions):
    quiz = Quiz(
        id=uuid4(),
        name="Sample Quiz",
        description="A sample quiz",
        _time=timedelta(minutes=30),
        difficulty=Difficulty.EASY,
        subject=subject,
        _questions=valid_questions,
    )

    with pytest.raises(ValueError, match="Quiz must have between 1 and 100 questions"):
        quiz.questions = []
