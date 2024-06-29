from sanic import Blueprint
from src.api.quiz_admin import quiz_admin


api = Blueprint.group(quiz_admin, url_prefix="/api")
