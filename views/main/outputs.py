import typing
from pydantic import BaseModel, validator


class TimeLog(BaseModel):
    timestamp: str
    event: str
    timer: str

    @validator('timestamp', pre=True)
    def datetime_to_str(cls, value):
        return value.isoformat()

    @validator('timer', pre=True)
    def timedelta_to_str(cls, value):
        return str(value)


class ConnectEvent(BaseModel):
    code: int = 100
    data: typing.List[TimeLog] = []


class ToggleEvent(BaseModel):
    code: int = 101
    data: TimeLog


class UpdateEvent(BaseModel):
    code: int = 102
    data: TimeLog
