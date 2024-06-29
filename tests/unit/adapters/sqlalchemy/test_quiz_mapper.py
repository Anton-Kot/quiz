from uuid import UUID
from datetime import timedelta
import pytest
from src.application.domain.quiz import Quiz, Subject, ChoiceQuestion, ChoiceAnswer, Difficulty
from src.adapters.sqlalchemy.models import QuizModel, SubjectModel
from src.adapters.sqlalchemy.mappers import QuizSQLAlchemyMapper


@pytest.fixture(name="quiz_mapper")
def quiz_mapper_f():
    return QuizSQLAlchemyMapper()


@pytest.fixture(name="sample_quiz")
def sample_quiz_f():
    subject = Subject(
        id=UUID("87654321-8765-4321-8765-432187654321"),
        name="Physics",
        description="Fundamental physics principles",
    )
    quiz = Quiz(
        id=UUID("11223344-5566-7788-99aa-bbccddee0011"),
        name="Physics Quiz",
        description="Advanced physics test",
        _time=timedelta(hours=1),
        difficulty=Difficulty.HARD,
        subject=subject,
        _questions=[
            ChoiceQuestion(
                id=UUID("aabbccdd-eeff-0011-2233-445566778899"),
                text="What is the speed of light?",
                _answers=[
                    ChoiceAnswer(
                        id=UUID("99999999-9999-9999-9999-999999999999"),
                        text="299,792,458 m/s",
                        is_correct=True,
                    ),
                    ChoiceAnswer(
                        id=UUID("88888888-8888-8888-8888-888888888888"),
                        text="300,000,000 m/s",
                        is_correct=False,
                    ),
                    ChoiceAnswer(
                        id=UUID("77777777-7777-7777-7777-777777777777"),
                        text="3,000,000 m/s",
                        is_correct=False,
                    ),
                ],
            ),
            ChoiceQuestion(
                id=UUID("11223344-5566-7788-99aa-bbccddee1122"),
                text="Who developed the theory of relativity?",
                _answers=[
                    ChoiceAnswer(
                        id=UUID("66666666-6666-6666-6666-666666666666"),
                        text="Albert Einstein",
                        is_correct=True,
                    ),
                    ChoiceAnswer(
                        id=UUID("55555555-5555-5555-5555-555555555555"), text="Isaac Newton", is_correct=False
                    ),
                ],
            ),
        ],
    )
    return quiz


@pytest.fixture(name="sample_quiz_model")
def sample_quiz_model_f(sample_quiz: Quiz):
    return QuizModel(
        id=sample_quiz.id,
        name=sample_quiz.name,
        description=sample_quiz.description,
        time=sample_quiz.time,
        difficulty=sample_quiz.difficulty,
        subject_id=sample_quiz.subject.id,
        subject=SubjectModel(
            id=sample_quiz.subject.id,
            name=sample_quiz.subject.name,
            description=sample_quiz.subject.description,
        ),
        questions=[
            {
                "id": str(q.id),
                "text": q.text,
                "answers": [{"id": str(a.id), "text": a.text, "is_correct": a.is_correct} for a in q.answers],
            }
            for q in sample_quiz.questions
        ],
    )


def test_domain_to_dict(quiz_mapper: QuizSQLAlchemyMapper, sample_quiz: Quiz):
    result = quiz_mapper.domain_to_dict(sample_quiz)
    assert result["id"] == sample_quiz.id
    assert result["name"] == sample_quiz.name
    assert result["description"] == sample_quiz.description
    assert result["time"] == sample_quiz.time
    assert result["difficulty"] == sample_quiz.difficulty
    assert result["subject_id"] == sample_quiz.subject.id
    assert len(result["questions"]) == len(sample_quiz.questions)
    assert result["questions"][0]["id"] == str(sample_quiz.questions[0].id)


def test_model_to_domain(quiz_mapper: QuizSQLAlchemyMapper, sample_quiz_model: QuizModel, sample_quiz: Quiz):
    result = quiz_mapper.model_to_domain(sample_quiz_model)
    assert result == sample_quiz
