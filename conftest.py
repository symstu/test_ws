import pytest
import logging

from alembic import command, config as alembic_config
from httpx import AsyncClient
from server import app
from settings import config
from utils.db import PgPool
from utils.testclient import AsyncioTestClient
from utils.event_loop import shared_event_loop


@pytest.fixture(scope='session')
def event_loop():
    return shared_event_loop


@pytest.fixture(scope='session', autouse=True)
async def db_instance():
    """Returns True if running on test database"""
    local_pool = PgPool(config.PG_DSN_ROOT)

    async with local_pool() as conn:
        await conn.execute('''
            SELECT
                pg_terminate_backend(pg_stat_activity.pid)
            FROM
                pg_stat_activity
            WHERE
                pg_stat_activity.datname = 'test_ws' AND
            pid <> pg_backend_pid();
        ''')
        await conn.execute(f"drop database if exists {config.PG_TEST_DB_NAME}")
        await conn.execute(f"create database {config.PG_TEST_DB_NAME}")

    alembic_conf = alembic_config.Config('alembic.ini')

    config.PG_DSN = config.PG_DSN
    alembic_conf.set_section_option(
        'alembic', 'sqlalchemy.url', config.PG_DSN)
    command.upgrade(alembic_conf, 'head')


@pytest.fixture(scope='session', autouse=True)
def update_config():
    from settings import config

    config.DEBUG = True
    config.MODE = 'testing'


@pytest.fixture(autouse=True)
def set_logging(caplog):
    caplog.set_level(logging.INFO, logger="crash")


@pytest.fixture(scope='session')
async def user_san_sanych():
    http_client = AsyncClient(
        app=app,
        base_url="http://testserver",
    )
    async with http_client as client:
        yield client


@pytest.fixture(scope='session')
async def user_gamaz():
    async with AsyncioTestClient(app, event_loop=shared_event_loop) as client:
        async with client.websocket_connect("/timer?u=1") as websocket:
            yield websocket


@pytest.fixture(scope='session')
async def user_bydlo():
    async with AsyncioTestClient(app, event_loop=shared_event_loop) as client:
        async with client.websocket_connect("/timer?u=2") as websocket:
            yield websocket
