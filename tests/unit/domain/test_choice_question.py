from uuid import uuid4
import pytest
from src.application.domain.quiz import ChoiceAnswer, ChoiceQuestion


def test_choice_question_creation_with_valid_data():
    answers = [ChoiceAnswer(id=uuid4(), text="Answer 1", is_correct=True)]
    question = ChoiceQuestion(id=uuid4(), text="Question 1", _answers=answers)
    assert question.answers == answers


def test_choice_question_creation_with_no_correct_answer():
    answers = [ChoiceAnswer(id=uuid4(), text="Answer 1", is_correct=False)]
    with pytest.raises(ValueError, match="At least one of the answers must be correct"):
        ChoiceQuestion(id=uuid4(), text="Question 1", _answers=answers)


def test_choice_question_creation_with_too_few_answers():
    answers = []
    with pytest.raises(ValueError, match="Answer count must be between 1 and 20"):
        ChoiceQuestion(id=uuid4(), text="Question 1", _answers=answers)


def test_choice_question_creation_with_too_many_answers():
    answers = [ChoiceAnswer(id=uuid4(), text=f"Answer {i+1}", is_correct=True) for i in range(21)]
    with pytest.raises(ValueError, match="Answer count must be between 1 and 20"):
        ChoiceQuestion(id=uuid4(), text="Question 1", _answers=answers)


def test_choice_question_change_answers_to_valid():
    answers = [ChoiceAnswer(id=uuid4(), text="Answer 1", is_correct=True)]
    question = ChoiceQuestion(id=uuid4(), text="Question 1", _answers=answers)

    new_answers = [
        ChoiceAnswer(id=uuid4(), text="Answer 2", is_correct=False),
        ChoiceAnswer(id=uuid4(), text="Answer 3", is_correct=True),
    ]
    question.answers = new_answers
    assert question.answers == new_answers


def test_choice_question_change_answers_to_no_correct():
    answers = [ChoiceAnswer(id=uuid4(), text="Answer 1", is_correct=True)]
    question = ChoiceQuestion(id=uuid4(), text="Question 1", _answers=answers)

    new_answers = [
        ChoiceAnswer(id=uuid4(), text="Answer 2", is_correct=False),
        ChoiceAnswer(id=uuid4(), text="Answer 3", is_correct=False),
    ]
    with pytest.raises(ValueError, match="At least one of the answers must be correct"):
        question.answers = new_answers


def test_choice_question_change_answers_to_too_many():
    answers = [ChoiceAnswer(id=uuid4(), text="Answer 1", is_correct=True)]
    question = ChoiceQuestion(id=uuid4(), text="Question 1", _answers=answers)

    new_answers = [ChoiceAnswer(id=uuid4(), text=f"Answer {i+1}", is_correct=True) for i in range(21)]
    with pytest.raises(ValueError, match="Answer count must be between 1 and 20"):
        question.answers = new_answers
