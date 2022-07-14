from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from views.main import handlers


def init(app: FastAPI):
    app.add_api_route(
        '/',
        handlers.main_page,
        methods=['GET'],
        response_class=HTMLResponse,
        description="Render main page"
    )

    app.add_api_websocket_route(
        '/timer',
        handlers.timer
    )
