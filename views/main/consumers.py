import asyncio

from datetime import datetime, time
from components.timer.models import Timer
from views.main import outputs
from views.main.manager import timer_manager
from utils.websockets import BaseConsumer


class TimerConsumer(BaseConsumer):
    async def on_connect(self):
        print(1)
        self.room.user_add(self.websocket)
        print(2)
        events = await Timer.all()
        print(3)
        await self.websocket.send_json(outputs.ConnectEvent(data=events).dict())
        print(4)

    async def on_toggle(self, data):
        timestamp = Timer.time()

        event_type = 1
        value = data.get('value')

        last_timer = await Timer.last()
        print('last timer', last_timer)

        if last_timer and last_timer['event']:
            event_type = 0

        print('event type', event_type)
        if event_type:
            timer_manager.run(self.room, timestamp)
        else:
            await timer_manager.stop(self.room, timestamp)

        asyncio.create_task(Timer.update(event_type, timestamp))

        print('toggle: ', data)

    async def on_disconnect(self):
        self.room.user_remove(self.websocket)

    async def on_error(self):
        return await self.on_disconnect()
