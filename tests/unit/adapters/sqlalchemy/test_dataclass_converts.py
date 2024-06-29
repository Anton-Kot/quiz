from dataclasses import asdict, dataclass
from datetime import timedelta
from uuid import UUID, uuid4

from sqlalchemy import Enum

from src.adapters.sqlalchemy.mappers import convert_dataclass_to_dict, convert_dict_to_serializable


@dataclass
class Level1:
    id: UUID
    name: str
    _hidden_attr: str


@dataclass
class Level2:
    id: UUID
    level1: Level1
    _hidden_attr: str


@dataclass
class Level3:
    id: UUID
    level2: Level2
    _hidden_attr: str


def test_convert_level1_dataclass():
    level1 = Level1(id=uuid4(), name="Level1", _hidden_attr="hidden")
    result = convert_dataclass_to_dict(level1)
    expected = {"id": level1.id, "name": "Level1", "hidden_attr": "hidden"}
    assert result == expected


def test_convert_level2_dataclass():
    level1 = Level1(id=uuid4(), name="Level1", _hidden_attr="hidden1")
    level2 = Level2(id=uuid4(), level1=level1, _hidden_attr="hidden2")
    result = convert_dataclass_to_dict(level2)
    expected = {
        "id": level2.id,
        "level1": {"id": level1.id, "name": "Level1", "hidden_attr": "hidden1"},
        "hidden_attr": "hidden2",
    }
    assert result == expected


def test_convert_level3_dataclass():
    level1 = Level1(id=uuid4(), name="Level1", _hidden_attr="hidden1")
    level2 = Level2(id=uuid4(), level1=level1, _hidden_attr="hidden2")
    level3 = Level3(id=uuid4(), level2=level2, _hidden_attr="hidden3")
    result = convert_dataclass_to_dict(level3)
    expected = {
        "id": level3.id,
        "level2": {
            "id": level2.id,
            "level1": {"id": level1.id, "name": "Level1", "hidden_attr": "hidden1"},
            "hidden_attr": "hidden2",
        },
        "hidden_attr": "hidden3",
    }
    assert result == expected


@dataclass
class SimpleClass:
    id: UUID
    name: str


@dataclass
class NestedClass:
    simple: SimpleClass
    duration: timedelta


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


@dataclass
class ComplexClass:
    id: UUID
    nested: NestedClass
    color: Color
    numbers: list[int]
    details: dict


def test_convert_simple_class():
    obj = SimpleClass(id=uuid4(), name="Test Name")
    result = convert_dict_to_serializable(asdict(obj))
    expected = {"id": str(obj.id), "name": "Test Name"}
    assert result == expected


def test_convert_nested_class():
    simple = SimpleClass(id=uuid4(), name="Nested Name")
    obj = NestedClass(simple=simple, duration=timedelta(minutes=5))
    result = convert_dict_to_serializable(asdict(obj))
    expected = {
        "simple": {"id": str(simple.id), "name": "Nested Name"},
        "duration": 300.0,  # 5 minutes in seconds
    }
    assert result == expected


def test_convert_complex_class():
    simple = SimpleClass(id=uuid4(), name="Simple Name")
    nested = NestedClass(simple=simple, duration=timedelta(minutes=10))
    obj = ComplexClass(
        id=uuid4(),
        nested=nested,
        color=Color.RED,
        numbers=[1, 2, 3],
        details={"key1": "value1", "key2": "value2"},
    )
    result = convert_dict_to_serializable(asdict(obj))
    expected = {
        "id": str(obj.id),
        "nested": {
            "simple": {"id": str(simple.id), "name": "Simple Name"},
            "duration": 600.0,  # 10 minutes in seconds
        },
        "color": "red",
        "numbers": [1, 2, 3],
        "details": {"key1": "value1", "key2": "value2"},
    }
    assert result == expected
