import typing
from datetime import datetime, time

from pydantic import BaseModel, validator


class TimeLog(BaseModel):
    timestamp: str
    event: str
    timer: str

    @validator('timestamp', pre=True)
    def datetime_to_str(cls, value):
        return value.strftime('%Y-%m-%d %H:%M:%S')

    @validator('timer', pre=True)
    def timedelta_to_str(cls, value):
        if isinstance(value, time):
            return value.strftime('%H:%M:%S')

        return datetime.utcfromtimestamp(value.seconds).strftime('%H:%M:%S')

    @validator('event', pre=True)
    def event_to_str(cls, value):
        if isinstance(value, str):
            return value

        if value:
            return 'started'

        return 'stopped'


class ConnectEvent(BaseModel):
    code: int = 100
    data: typing.List[TimeLog] = []


class ToggleEvent(BaseModel):
    code: int = 101
    data: TimeLog


class UpdateEvent(BaseModel):
    code: int = 102
    data: TimeLog
