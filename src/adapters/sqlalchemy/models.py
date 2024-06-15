from datetime import timedelta
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Interval, String, Text, Uuid
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from src.application.domain.quiz import Difficulty
from src.adapters.sqlalchemy.connect import Base


class SubjectModel(Base):
    __tablename__ = "subject"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class QuizModel(Base):
    __tablename__ = "quiz"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    time: Mapped[timedelta] = mapped_column(Interval, nullable=False)
    difficulty: Mapped[Difficulty] = mapped_column(Enum(Difficulty), nullable=False)
    subject_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("subject.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False
    )
    questions: Mapped[list[JSONB]] = mapped_column(ARRAY(JSONB), nullable=False)
