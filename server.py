from fastapi import FastAPI

from views.main.router import init as main_router
from views.main.on_startup import start_timer

app = FastAPI()
main_router(app)


@app.on_event('startup')
async def run():
    from utils.websockets import room
    await start_timer(room)
