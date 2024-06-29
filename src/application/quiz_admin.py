from dataclasses import dataclass
from typing import Optional, Protocol
from datetime import timedelta
from uuid import UUID, uuid4
from src.application.ports.quiz import QuizRepository
from src.application.ports.subject import SubjectRepository
from src.application.domain.quiz import ChoiceAnswer, ChoiceQuestion, Difficulty, Quiz, Subject
from src.application.ports.uow import UnitOfWork


@dataclass
class SubjectDTO:
    name: str
    description: str
    id: Optional[UUID] = None


@dataclass
class QuizAdminDTO:
    name: str
    description: str
    time: timedelta
    difficulty: Difficulty
    subject: Subject
    questions: list["ChoiceQuestionAdminDTO"]
    id: Optional[UUID] = None


@dataclass
class ChoiceQuestionAdminDTO:
    text: str
    answers: list["ChoiceAnswerAdminDTO"]
    id: Optional[UUID] = None


@dataclass
class ChoiceAnswerAdminDTO:
    is_correct: bool
    text: str
    id: Optional[UUID] = None


class DomainMapper(Protocol):
    def map_dto_to_domain_object(self, dto):
        pass

    def map_domain_object_to_dto(self, domain_object):
        pass


class SubjectDomainMapper:
    def map_dto_to_domain_object(self, dto: SubjectDTO):
        object_id = dto.id if dto.id else uuid4()
        return Subject(id=object_id, name=dto.name, description=dto.description)

    def map_domain_object_to_dto(self, domain_object: Subject):
        return SubjectDTO(id=domain_object.id, name=domain_object.name, description=domain_object.description)


class QuizDomainMapper:
    def map_dto_to_domain_object(self, dto: QuizAdminDTO):
        questions = []
        for question in dto.questions:
            q_id = question.id if question.id else uuid4()
            if isinstance(question, ChoiceQuestionAdminDTO):
                answers = []
                for answer in question.answers:
                    a_id = answer.id if answer.id else uuid4()
                    if isinstance(answer, ChoiceAnswerAdminDTO):
                        answers.append(ChoiceAnswer(id=a_id, is_correct=answer.is_correct, text=answer.text))
                    else:
                        raise ValueError("Invalid answer type")
                questions.append(
                    ChoiceQuestion(
                        id=q_id,
                        text=question.text,
                        _answers=answers,
                    )
                )
            else:
                raise ValueError("Invalid question type")

        object_id = dto.id if dto.id else uuid4()
        return Quiz(
            id=object_id,
            name=dto.name,
            description=dto.description,
            _time=dto.time,
            difficulty=dto.difficulty,
            subject=dto.subject,
            _questions=questions,
        )

    def map_domain_object_to_dto(self, domain_object: Quiz):
        questions = []
        for question in domain_object.questions:
            if isinstance(question, ChoiceQuestion):
                for answer in question.answers:
                    if isinstance(answer, ChoiceAnswer):
                        questions.append(
                            ChoiceQuestionAdminDTO(
                                id=question.id,
                                text=question.text,
                                answers=[
                                    ChoiceAnswerAdminDTO(
                                        id=answer.id, is_correct=answer.is_correct, text=answer.text
                                    )
                                ],
                            )
                        )
                    else:
                        raise ValueError("Invalid answer type")
            else:
                raise ValueError("Invalid question type")

        return QuizAdminDTO(
            id=domain_object.id,
            name=domain_object.name,
            description=domain_object.description,
            time=domain_object.time,
            difficulty=domain_object.difficulty,
            subject=domain_object.subject,
            questions=questions,
        )


class BaseAdminService:
    uow: UnitOfWork
    domain_mapper: DomainMapper

    def __init__(self, uow, repo, domain_mapper):
        self.uow = uow
        self.repo = repo
        self.domain_mapper = domain_mapper

    async def create_one(self, dto):
        async with self.uow as uow:
            new_object = self.domain_mapper.map_dto_to_domain_object(dto)
            created = await self.repo.add_one(new_object)
            await uow.commit()
            return created

    async def get_all(self):
        async with self.uow:
            objects = await self.repo.get_all()
            return [self.domain_mapper.map_domain_object_to_dto(obj) for obj in objects]

    async def update_one(self, object_id, dto):
        async with self.uow as uow:
            dto.id = object_id
            updated_object = self.domain_mapper.map_dto_to_domain_object(dto)
            updated = await self.repo.update_one(object_id, updated_object)
            await uow.commit()
            return updated

    async def delete_one(self, object_id: UUID) -> UUID:
        async with self.uow as uow:
            deleted = await self.repo.delete_one(object_id)
            await uow.commit()
            return deleted


class SubjectAdminService:
    uow: UnitOfWork
    repo: SubjectRepository

    def __init__(self, uow: UnitOfWork, repo: SubjectRepository):
        self.uow = uow
        self.repo = repo
        self.base_service = BaseAdminService(uow, repo, SubjectDomainMapper())

    async def create_one(self, subject_dto: SubjectDTO) -> UUID:
        return await self.base_service.create_one(subject_dto)

    async def get_all(self) -> list[SubjectDTO]:
        return await self.base_service.get_all()

    async def update_one(self, subject_id, subject_dto: SubjectDTO) -> UUID:
        return await self.base_service.update_one(subject_id, subject_dto)

    async def delete_one(self, subject_id: UUID) -> UUID:
        return await self.base_service.delete_one(subject_id)


class QuizAdminService:
    uow: UnitOfWork
    repo: QuizRepository

    def __init__(self, uow: UnitOfWork, repo: QuizRepository):
        self.uow = uow
        self.repo = repo
        self.base_service = BaseAdminService(uow, repo, QuizDomainMapper())

    async def create_one(self, quiz_dto: QuizAdminDTO) -> UUID:
        return await self.base_service.create_one(quiz_dto)

    async def get_all(self) -> list[QuizAdminDTO]:
        return await self.base_service.get_all()

    async def update_one(self, quiz_id, quiz_dto: QuizAdminDTO) -> UUID:
        return await self.base_service.update_one(quiz_id, quiz_dto)

    async def delete_one(self, quiz_id: UUID) -> UUID:
        return await self.base_service.delete_one(quiz_id)
