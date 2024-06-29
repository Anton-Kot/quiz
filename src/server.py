from textwrap import dedent
from sanic import Sanic
from orjson import dumps, loads  # pylint: disable=E0611
from src.dependencies import add_dependencies
from src.config import APP_NAME
from src.config import CORS_ORIGINS
from src.api.api import api


def create_app() -> Sanic:
    app = Sanic(APP_NAME, dumps=dumps, loads=loads)

    app.config.OAS_UI_DEFAULT = "swagger"
    app.ext.openapi.describe(
        "Quiz API",
        version="1.0.0",
        description=dedent(
            """
            Quiz API Documentation
            """
        ),
    )
    app.config.RESPONSE_TIMEOUT = 30
    app.config.CORS_ORIGINS = CORS_ORIGINS

    app.blueprint(api)

    add_dependencies(app)

    return app
