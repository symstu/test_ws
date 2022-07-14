import asyncio


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
