from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID
from typing import List
from sanic import Blueprint, Request, json
from sanic_ext import validate, openapi
from sanic_ext.extensions.openapi.definitions import Response
from pydantic import BaseModel
from src.application.quiz_admin import SubjectAdminService, SubjectDTO
from src.application.domain.quiz import Difficulty, Subject


quiz_admin = Blueprint("quiz-admin", url_prefix="/quiz-admin")


class SubjectModel(BaseModel):
    name: str
    description: str


class ChoiceAnswerModel(BaseModel):
    is_correct: bool
    text: str


class ChoiceQuestionModel(BaseModel):
    text: str
    answers: List[ChoiceAnswerModel]


class QuizModel(BaseModel):
    name: str
    description: str
    time: timedelta
    difficulty: Difficulty
    subject: Subject
    questions: List[ChoiceQuestionModel]


@dataclass
class UuidResponseModel:
    id: UUID


@dataclass
class SubjectResponseModel:
    id: UUID
    name: str
    description: str


openapi_subject_create = openapi.definition(
    body={"application/json": SubjectModel.model_json_schema(ref_template="#/components/schemas/{model}")},
    response=[
        Response(
            status="201",
            content={
                "application/json": UuidResponseModel,
            },
            description="Success create",
        )
    ],
    summary="Create a new subject",
    tag="Subject",
)


openapi_subject_getall = openapi.definition(
    response=[
        Response(
            status="200",
            content={
                "application/json": list[SubjectResponseModel],
            },
            description="Success response",
        )
    ],
    summary="Get all subjects",
    tag="Subject",
)


openapi_subject_update = openapi.definition(
    parameter={
        "name": "subject_id",
        "schema": UUID,
        "required": True,
        "location": "path",
    },
    body={"application/json": SubjectModel.model_json_schema(ref_template="#/components/schemas/{model}")},
    response=[
        Response(
            status="200",
            content={
                "application/json": UuidResponseModel,
            },
            description="Success response",
        )
    ],
    summary="Update a subject",
    tag="Subject",
)


@quiz_admin.post("/subject")
@openapi_subject_create
@validate(json=SubjectModel)
async def create_subject(_: Request, body: SubjectModel, subject_service: SubjectAdminService):
    subject_id = await subject_service.create_one(SubjectDTO(**body.model_dump()))
    return json(UuidResponseModel(id=subject_id), status=201)


@quiz_admin.get("/subject")
@openapi_subject_getall
async def get(_: Request, subject_service: SubjectAdminService):
    subjects = await subject_service.get_all()
    return json(subjects)


@quiz_admin.put("/subject/<subject_id>")
@openapi_subject_update
@validate(json=SubjectModel)
async def put(_: Request, subject_id: UUID, body: SubjectModel, subject_service: SubjectAdminService):
    updated_id = await subject_service.update_one(subject_id, SubjectDTO(**body.model_dump()))
    return json({"id": str(updated_id)})


@openapi.definition(
    parameter={
        "name": "body",
    },
    body={"application/json": SubjectModel.model_json_schema(ref_template="#/components/schemas/{model}")},
)
async def delete(_: Request, subject_id: UUID, subject_service: SubjectAdminService):
    deleted_id = await subject_service.delete_one(subject_id)
    return json({"id": str(deleted_id)})


# # Quiz routes
# @quiz_admin.post("/quizzes")
# @inject
# @validate(json=QuizModel)
# async def create_quiz(
#     request, body: QuizModel, quiz_service: QuizAdminService = Provide[Container.quiz_admin_service]
# ):
#     quiz_id = await quiz_service.create_one(QuizAdminDTO(**body.dict()))
#     return json({"id": str(quiz_id)}, status=201)


# @quiz_admin.get("/quizzes")
# @inject
# async def get_all_quizzes(request, quiz_service: QuizAdminService = Provide[Container.quiz_admin_service]):
#     quizzes = await quiz_service.get_all()
#     return json([quiz.dict() for quiz in quizzes])


# @quiz_admin.put("/quizzes/<quiz_id:uuid>")
# @inject
# @validate(json=QuizModel)
# async def update_quiz(
#     request,
#     quiz_id: UUID,
#     body: QuizModel,
#     quiz_service: QuizAdminService = Provide[Container.quiz_admin_service],
# ):
#     updated_id = await quiz_service.update_one(quiz_id, QuizAdminDTO(**body.dict()))
#     return json({"id": str(updated_id)})


# @quiz_admin.delete("/quizzes/<quiz_id:uuid>")
# @inject
# async def delete_quiz(
#     request, quiz_id: UUID, quiz_service: QuizAdminService = Provide[Container.quiz_admin_service]
# ):
#     deleted_id = await quiz_service.delete_one(quiz_id)
#     return json({"id": str(deleted_id)})
