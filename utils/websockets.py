import asyncio
import traceback

from starlette.websockets import WebSocketDisconnect

from fastapi import WebSocket
from pydantic import BaseModel


def frange(start, to, step):
    while start < to:
        start += step
        yield start


class WebsocketRoom:
    def __init__(self):
        self.websockets = dict()

    async def publish(self, message: dict):
        coroutines = []

        for websocket in self.websockets.values():
            coroutines.append(websocket.send_json(message))

        await asyncio.gather(*coroutines)

    async def send(self, websocket, message: dict):
        await websocket.send_json(message)

    def user_add(self, websocket):
        self.websockets[self.__user_key(websocket)] = websocket

    def reset(self):
        self.websockets = dict()

    def user_remove(self, websocket):
        self.websockets.pop(self.__user_key(websocket))

    @staticmethod
    def __user_key(websocket):
        return f'{websocket.client.host}:{websocket.client.port}'\
               f':{websocket.query_params}'


class WebsocketError(BaseModel):
    message: str


class BaseConsumer:
    def __init__(self, room,websocket):
        self.websocket: WebSocket = websocket
        self.room = room

    async def run(self):
        try:
            await self.websocket.accept()
            await self.on_connect()
            await self.__receive_json()
        except Exception as e:
            # logger.error(traceback.format_exc())
            print(traceback.format_exc())
            await self.on_error()

    async def __receive_json(self):
        while True:
            try:
                data = await self.websocket.receive_json()
                action = data.get('action')

                if not action:
                    continue

                try:
                    event = self.__getattribute__(f'on_{action}')

                except AttributeError:
                    await self.send_error("unknown action")
                    continue

                # if event:
                await event(data=data)

            except WebSocketDisconnect:
                await self.on_disconnect()
                return

    async def on_connect(self):
        pass

    async def on_disconnect(self):
        pass

    async def on_error(self):
        pass

    async def send_error(self, message: str):
        return await self.websocket.send_json(
            WebsocketError(message=message).dict()
        )


room = WebsocketRoom()
