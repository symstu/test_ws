import asyncio

from datetime import datetime, timedelta
from views.main import outputs


class TimerManager:
    def __init__(self):
        self.timestamp = None
        self.task = None

    def run(self, room, timestamp):
        self.timestamp = timestamp
        self.task = asyncio.create_task(self.__start(room))
        print('task created : ', self.task)

    async def stop(self, room, timestamp):
        await room.publish(outputs.UpdateEvent(data={
            'timestamp': timestamp,
            'time': self.__get_time(timestamp, self.timestamp),
            'event': 'stopped'
        }))

        self.task.cancel()

    async def __start(self, room):
        await room.publish(outputs.ToggleEvent(data={
            'timestamp': self.timestamp,
            'time': '00:00:00',
            'event': 'started'
        }))

        while True:
            await asyncio.sleep(0.5)

            data = outputs.UpdateEvent(data={
                'timestamp': self.timestamp,
                'time': self.__get_time(datetime.utcnow(), self.timestamp),
                'event': 'started'
            })
            print('updated timer: ', data)
            await room.publish(data)

    def __get_time(self, timestamp_now, timestamp_before):
        return datetime.fromtimestamp((timestamp_now - timestamp_before).seconds).isoformat()


timer_manager = TimerManager()
