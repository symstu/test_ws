import asyncio

from components.timer.models import Timer
from views.main import outputs
from views.main.manager import timer_manager
from utils.websockets import BaseConsumer


class TimerConsumer(BaseConsumer):
    def __init__(self, room, websocket):
        super(TimerConsumer, self).__init__(room, websocket)
        self.counter = 0

    async def on_connect(self):
        self.room.user_add(self.websocket)
        events = await Timer.all()
        await self.websocket.send_json(
            outputs.ConnectEvent(data=events).dict())

    async def on_toggle(self, data):
        self.counter += 1

        if not self.counter % 3:
            return

        timestamp = Timer.time()
        event_type = 1

        last_timer = await Timer.last()

        if last_timer and last_timer['event']:
            event_type = 0

        if event_type:
            timer_manager.run(self.room, timestamp)
            asyncio.create_task(Timer.create(timestamp))
        else:
            await timer_manager.stop(self.room, timestamp)
            asyncio.create_task(Timer.stop(last_timer['id'], timestamp))

    async def on_clear(self, data):
        await timer_manager.stop(self.room, Timer.time())
        await Timer.delete()

    async def on_disconnect(self):
        self.room.user_remove(self.websocket)

    async def on_error(self):
        return await self.on_disconnect()
