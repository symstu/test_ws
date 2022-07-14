import sqlalchemy as sa
from utils.db_sync import Base


class Timer(Base):
    __tablename__ = 'timers'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    value: str = sa.Column(sa.DateTime, nullable=False)
