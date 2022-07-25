from enum import Enum
from datetime import datetime, time

import sqlalchemy as sa
from sqlalchemy import text

from utils.db_sync import Base
from utils.db import adb_session


class EventType(int, Enum):
    started: bool = 1
    paused: bool = 0


class Timer(Base):
    __tablename__ = 'timers'

    id: int = sa.Column(
        sa.Integer,
        primary_key=True,
        autoincrement=True
    )
    event: int = sa.Column(
        sa.Integer,
        nullable=False,
        server_default=f'{EventType.started.value}'
    )
    timestamp: datetime = sa.Column(
        sa.DateTime,
        server_default=text('current_timestamp')
    )
    timer: time = sa.Column(
        sa.Time,
        nullable=False
    )

    @classmethod
    async def all(cls):
        async with adb_session() as conn:
            return await conn.fetch('SELECT * FROM timers')

    @classmethod
    async def last(cls):
        async with adb_session() as conn:
            return await conn.fetchrow(
                'SELECT * FROM timers ORDER BY id DESC LIMIT 1')

    @classmethod
    def time(cls):
        return datetime.utcnow()

    @classmethod
    async def create(cls, timestamp: time):
        async with adb_session() as conn:
            return await conn.execute(
                '''
                INSERT INTO timers (event, timestamp, timer) 
                VALUES ($1, $2, $3)
                ''',
                1,
                timestamp,
                time.fromisoformat('00:00:00')
            )

    @classmethod
    async def stop(cls, record_id: int, timestamp: time):
        async with adb_session() as conn:
            return await conn.execute(
                '''
                UPDATE timers 
                SET event = 0, 
                    timer = $1::timestamp - timestamp
                WHERE id = $2
                ''',
                timestamp,
                record_id
            )

    @classmethod
    async def delete(cls):
        async with adb_session() as conn:
            return await conn.execute('DELETE FROM timers')
