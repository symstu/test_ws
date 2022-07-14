from components.timer.models import Timer
from views.main.manager import timer_manager


async def start_timer(room):
    last_timer = await Timer.last()

    if not last_timer:
        return None

    if not last_timer['event']:
        return None

    timer_manager.run(room, last_timer['timestamp'])
