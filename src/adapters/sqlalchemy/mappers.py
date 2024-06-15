from dataclasses import fields, is_dataclass
from datetime import timedelta
from typing import Protocol
from uuid import UUID

from sqlalchemy import Enum

from src.application.domain.quiz import Quiz, Subject


def convert_dataclass_to_dict(obj):
    if isinstance(obj, list):
        return [convert_dataclass_to_dict(item) for item in obj]
    elif is_dataclass(obj):
        result = {}
        for field in fields(obj):
            field_name = field.name
            field_value = getattr(obj, field_name)
            new_key = field_name.lstrip('_')
            result[new_key] = convert_dataclass_to_dict(field_value)
        return result
    else:
        return obj


def convert_dict_to_serializable(obj: dict) -> dict:
    if isinstance(obj, list):
        return [convert_dict_to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_dict_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, timedelta):
        return obj.total_seconds()
    elif isinstance(obj, Enum):
        return obj.value
    else:
        return obj


class SQLAlchemyMapper(Protocol):
    def domain_to_dict(self, domain_object): ...


class SubjectSQLAlchemyMapper(SQLAlchemyMapper):
    def domain_to_dict(self, domain_object: Subject):
        return convert_dataclass_to_dict(domain_object)


class QuizSQLAlchemyMapper(SQLAlchemyMapper):
    def domain_to_dict(self, domain_object: Quiz):
        dict_quiz = convert_dataclass_to_dict(domain_object)
        dict_quiz['questions'] = convert_dict_to_serializable(dict_quiz['questions'])
        dict_quiz['subject_id'] = dict_quiz.pop('subject')["id"]
        return dict_quiz
