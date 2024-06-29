from dataclasses import dataclass
from datetime import timedelta
from enum import auto, StrEnum
from uuid import UUID


class Difficulty(StrEnum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


@dataclass
class Subject:
    id: UUID
    name: str
    description: str


@dataclass
class BaseQuestion:
    id: UUID
    text: str


@dataclass
class BaseAnswer:
    id: UUID


@dataclass
class ChoiceAnswer(BaseAnswer):
    is_correct: bool
    text: str


@dataclass
class ChoiceQuestion(BaseQuestion):
    _answers: list[ChoiceAnswer]

    def __post_init__(self):
        self._validate_answers(self._answers)

    @property
    def answers(self):
        return self._answers

    @answers.setter
    def answers(self, values: list[ChoiceAnswer]):
        self._validate_answers(values)
        self._answers = values

    def _validate_answers(self, answers: list[ChoiceAnswer]):
        self._check_answer_count(answers)
        self._check_at_least_one_answer_correct(answers)

    def _check_at_least_one_answer_correct(self, answers: list[ChoiceAnswer]):
        if not any(answer.is_correct for answer in answers):
            raise ValueError("At least one of the answers must be correct")

    def _check_answer_count(self, answers: list[ChoiceAnswer]):
        lower_bound = 1
        upper_bound = 20
        if not lower_bound <= len(answers) <= upper_bound:
            raise ValueError(f"Answer count must be between {lower_bound} and {upper_bound}")


@dataclass
class Quiz:
    id: UUID
    name: str
    description: str
    _time: timedelta
    difficulty: Difficulty
    subject: Subject
    _questions: list[BaseQuestion]
    # BaseQuestion: нарушение LSP, слишком общий родитель не отражающий сути наследников.
    # => нарушение OCP, т.к. Quiz начинает иметь специфику вида Question.

    def __post_init__(self):
        self._validate_time(self._time)
        self._validate_questions_count(self._questions)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value: timedelta):
        self._validate_time(value)
        self._time = value

    @property
    def questions(self):
        return self._questions

    @questions.setter
    def questions(self, value: list):
        self._validate_questions_count(value)
        self._questions = value

    def _validate_time(self, time: timedelta):
        lower_bound = timedelta(minutes=1)
        upper_bound = timedelta(minutes=240)
        if not lower_bound <= time <= upper_bound:
            raise ValueError(f"Quiz time must be between {lower_bound} and {upper_bound}")

    def _validate_questions_count(self, questions: list):
        lower_bound = 1
        upper_bound = 100
        if not lower_bound <= len(questions) <= upper_bound:
            raise ValueError(f"Quiz must have between {lower_bound} and {upper_bound} questions")
