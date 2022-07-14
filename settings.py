from pydantic import BaseSettings


class Settings(BaseSettings):
    PG_DSN: str = 'postgresql://postgres:postgres@localhost:5432/test_ws'
    DEBUG: bool = True
    MODE: str = 'dev'
    HOST: str = 'http://localhost:8000'

    class Config:
        env_file = '.env'


config = Settings()
