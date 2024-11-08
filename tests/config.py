
import os
from dotenv import load_dotenv


load_dotenv()


TEST_POSTGRE_HOST = os.getenv("TEST_POSTGRE_HOST")
TEST_POSTGRE_PORT = os.getenv("TEST_POSTGRE_PORT")
TEST_POSTGRE_DB_NAME = os.getenv("TEST_POSTGRE_DB_NAME")
TEST_POSTGRE_USERNAME = os.getenv("TEST_POSTGRE_USERNAME")
TEST_POSTGRE_PASSWORD = os.getenv("TEST_POSTGRE_PASSWORD")
