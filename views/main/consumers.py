import asyncio

from components.timer.models import Timer
from views.main import outputs
from views.main.manager import timer_manager
from utils.websockets import BaseConsumer


class TimerConsumer(BaseConsumer):
    async def on_connect(self):
        self.room.user_add(self.websocket)
        events = await Timer.all()
        await self.websocket.send_json(
            outputs.ConnectEvent(data=events).dict())

    async def on_toggle(self, data):
        print('toggle')
        timestamp = Timer.time()
        event_type = 1

        last_timer = await Timer.last()

        print('toggle 1')
        if last_timer and last_timer['event']:
            event_type = 0

        if event_type:
            timer_manager.run(self.room, timestamp)
            asyncio.create_task(Timer.create(timestamp))
            print('current loop id', id(asyncio.get_event_loop()))
            print('toggle 2')
        else:
            await timer_manager.stop(self.room, timestamp)
            asyncio.create_task(Timer.stop(last_timer['id'], timestamp))
            print('toggle 3')

    async def on_disconnect(self):
        self.room.user_remove(self.websocket)

    async def on_error(self):
        return await self.on_disconnect()
