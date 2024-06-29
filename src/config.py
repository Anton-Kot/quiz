import os

from dotenv import load_dotenv


load_dotenv()

POSTGRE_HOST = os.getenv("POSTGRE_HOST")
POSTGRE_PORT = os.getenv("POSTGRE_PORT")
POSTGRE_DB_NAME = os.getenv("POSTGRE_DB_NAME")
POSTGRE_USERNAME = os.getenv("POSTGRE_USERNAME")
POSTGRE_PASSWORD = os.getenv("POSTGRE_PASSWORD")

CORS_ORIGINS = os.getenv("CORS_ORIGINS")

APP_NAME = "quiz-service"
