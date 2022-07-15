from fastapi import (
    Request,
    WebSocket
)
from fastapi.templating import Jinja2Templates

from views.main.consumers import TimerConsumer
from utils.websockets import room
from settings import config


templates = Jinja2Templates(directory="templates")


async def main_page(request: Request):
    return templates.TemplateResponse('main.html', {
        'request': request,
        'host': config.HOST
    })


async def timer(websocket: WebSocket):
    await TimerConsumer(room, websocket).run()
