from components.timer.models import Timer
from views.main.manager import timer_manager


async def start_timer(room):
    print('staring timer...')
    last_timer = await Timer.last()

    print('last timer', last_timer)

    if not last_timer:
        return None

    if not last_timer['event']:
        return None

    timer_manager.run(room, last_timer['timestamp'])
