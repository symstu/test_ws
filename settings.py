from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    MODE: str = 'dev'
    HOST: str = 'localhost:8000'

    PG_DSN: str = 'postgresql://postgres:postgres@localhost:5432/test_ws'
    PG_DSN_ROOT: str = 'postgresql://postgres:postgres@localhost:5432/postgres'
    PG_TEST_DB_NAME: str = 'test_ws'

    class Config:
        env_file = '.env'


config = Settings()
