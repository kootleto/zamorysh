import functools
import time

from config import settings
from engine.schema import GameState, ActivityOptions

_ui_wait_time = 0.0

if settings.gui:
    from .gui import gui
    interface = gui
else:
    from .cli import cli
    interface = cli


def record_wait_time(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        global _ui_wait_time

        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()

        _ui_wait_time += end - start

        return result

    return wrapper


def pop_wait_time():
    global _ui_wait_time

    total = _ui_wait_time
    _ui_wait_time = 0.0
    return total


def display(*message, sep: str = " "):
    interface.display(*message, sep=sep)


@record_wait_time
async def prompt(*message, sep: str = " ") -> str:
    response = await interface.prompt(*message, sep=sep)
    return response


@record_wait_time
async def prompt_activity(options: ActivityOptions) -> int:
    index = await interface.prompt_activity(options)
    return index


def refresh_stats(gs: GameState):
    interface.refresh_stats(gs)


def check_button_pressed():
    return interface.check_button_pressed()


async def on_finish():
    await interface.on_finish()
