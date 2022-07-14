import asyncio

from datetime import datetime
from views.main import outputs
from utils.logging import get_logger


logger = get_logger('ws')


class TimerManager:
    def __init__(self):
        self.timestamp = None
        self.task = None

    def run(self, room, timestamp):
        self.timestamp = timestamp
        self.task = asyncio.create_task(self.__start(room))
        logger.info(f'task created: {timestamp}')

    async def stop(self, room, timestamp):
        await room.publish(outputs.UpdateEvent(data={
            'timestamp': self.timestamp,
            'timer': self.__get_time(timestamp, self.timestamp),
            'event': 'stopped'
        }).dict())

        self.task.cancel()
        logger.info('task stopped')

    async def __start(self, room):
        logger.info('tick time')
        await room.publish(outputs.ToggleEvent(data={
            'timestamp': self.timestamp,
            'timer': self.__get_time(self.timestamp, self.timestamp),
            'event': 'started'
        }).dict())

        while True:
            await asyncio.sleep(0.5)
            data = outputs.UpdateEvent(data={
                'timestamp': self.timestamp,
                'timer': self.__get_time(datetime.utcnow(), self.timestamp),
                'event': 'started'
            }).dict()
            await room.publish(data)
            logger.info(f'updated timer: {data}')

    def __get_time(self, timestamp_now, timestamp_before):
        return timestamp_now - timestamp_before


timer_manager = TimerManager()
