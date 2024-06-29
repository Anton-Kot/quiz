
from argparse import Namespace
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Union
import pytest
import pytest_asyncio
from alembic.config import Config
from tests.integration.sqlalchemy.connect import create_database, drop_models, init_models


PROJECT_PATH = Path(__file__).parent.parent.parent.parent.resolve()


def make_alembic_config(cmd_opts: Union[Namespace, SimpleNamespace],
                        base_path: str = PROJECT_PATH) -> Config:
    """
    Snippet from https://github.com/alvassin/backendschool2019/blob/master/analyzer/utils/pg.py

    Создает объект конфигурации alembic на основе аргументов командной строки,
    подменяет относительные пути на абсолютные.
    """
    # Подменяем путь до файла alembic.ini на абсолютный
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name,
                    cmd_opts=cmd_opts)

    # Подменяем путь до папки с alembic на абсолютный
    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location',
                               os.path.join(base_path, alembic_location))
    if cmd_opts.db_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.db_url)

    return config


@pytest.fixture(scope="module", name="real_alembic_config")
def real_alembic_config_f(db_url):
    """
    Создает объект с конфигурацией для alembic, настроенный на временную БД.
    """
    cmd_options = SimpleNamespace(config='alembic.ini', name='alembic',
                                  db_url=db_url, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest_asyncio.fixture(scope="module", autouse=True)
async def create_test_database(real_alembic_config: Config):
    print("Creating test database...")
    await create_database()
    await init_models(real_alembic_config)
    yield
    await drop_models(real_alembic_config)
    print("Test database dropped.")
