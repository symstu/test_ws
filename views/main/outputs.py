import typing
from datetime import datetime, time
from pydantic import BaseModel, validator


class TimeLog(BaseModel):
    timestamp: str
    event: str
    timer: str

    @validator('timestamp', 'timer', pre=True)
    def to_str(cls, value):
        return value.isoformat()


class ConnectEvent(BaseModel):
    code: int = 100
    data: typing.List[TimeLog] = []


class ToggleEvent(BaseModel):
    code: int = 101
    data: TimeLog


class UpdateEvent(BaseModel):
    code: int = 102
    data: TimeLog
