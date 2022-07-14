import asyncpg

from settings import config


class PgPool():
    def __init__(self, dsn: str):
        self.__pool = None
        self.dsn = dsn

    async def __call__(self):
        if not self.__pool:
            self.__pool = await asyncpg.create_pool(
                dsn=self.dsn,
                command_timeout=60,
            )

        async with self.__pool.acquire() as con:
            yield con


adb_session = PgPool(config.PG_DSN)
