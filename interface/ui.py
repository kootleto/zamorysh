import functools
import time
from typing import Callable

from config import SETTINGS
from engine.schema import GameState, ActivityOptions

_ui_wait_time = 0.0

if SETTINGS.gui:
    from .gui import gui

    interface = gui
else:
    from .cli import cli

    interface = cli


def _record_wait_time(func):
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


def init_ui():
    return interface.init_ui()


def display(*message, sep: str = " "):
    interface.display(*message, sep=sep)


def display_at(gs, *message, sep: str = " "):
    interface.display_at(gs, *message, sep=sep)


@_record_wait_time
async def prompt_activity(options: ActivityOptions) -> int:
    index = await interface.prompt_activity(options)
    return index


@_record_wait_time
async def ask_option(
    options,
    message,
    submit_required=False,
    submit_message: str | Callable[[int], str] | None = None,
    cols=3,
):
    option = await interface.ask_option(
        options, message, submit_required, submit_message, cols
    )
    return option


def refresh_ui(gs: GameState, options: ActivityOptions):
    interface.refresh_ui(gs, options)


def check_button_pressed():
    return interface.check_button_pressed()


async def on_finish():
    await interface.on_finish()
