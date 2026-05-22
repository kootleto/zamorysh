import asyncio
from copy import deepcopy
from typing import TypedDict

from kivy.app import App

from engine.schema import ActivityOptions, GameState
from gameplay.api import vitals, stats, time, music, location


class AppProxy:
    def __getattr__(self, name):
        return getattr(App.get_running_app(), name)

    def __setattr__(self, name, value):
        setattr(App.get_running_app(), name, value)


app = AppProxy()


class KivyState(TypedDict):
    track_title: str | None
    volume: int
    fullscreen: bool


INITIAL_UI_STATE: KivyState = {"track_title": None, "volume": 100, "fullscreen": False}


def init_ui() -> KivyState:
    return deepcopy(INITIAL_UI_STATE)


def display(*message, sep: str = " "):

    message = sep.join(map(str, message))
    app.root.ids.logger.add_line(message)


async def prompt(*message, sep: str = " ") -> str:
    app_input = app.root.ids.input

    message = sep.join(map(str, message))

    app_input.focus = True
    app_input.disabled = False
    app_input.hint_text = message
    await _wait_for_event(app.root.ids.button, "on_press")
    response = app_input.text
    app_input.text = ""
    app_input.hint_text = ""
    app_input.disabled = True

    return response


async def prompt_activity(options: ActivityOptions) -> int:
    activity_list = app.root.ids.activity_list
    button = app.root.ids.button

    activity_list.selected_index = -1
    button.text = "Выберите активность"
    activity_list.items = [option["label"] for option in options]

    await _wait_for_event(button, "on_press")
    while activity_list.selected_index == -1:
        button.text = "Сначала нужно выбрать активность!"
        await _wait_for_event(button, "on_press")

    button.text = "Игра запущена"
    index = activity_list.selected_index
    activity_list.selected_index = -1
    return index


def refresh_ui(gs: GameState, options: ActivityOptions):
    app.stats = {
        "datetime": time.get_datetime(gs),
        "location": {
            "place": location.get_place(gs),
            "x": location.get(gs, location.X),
            "y": location.get(gs, location.Y),
        },
        "fatigue": vitals.get(gs, vitals.FATIGUE),
        "money": stats.get(gs, stats.MONEY),
        "social": stats.get(gs, stats.SOCIAL),
        "mental": vitals.get(gs, vitals.MENTAL),
        "knowledge": stats.get(gs, stats.KNOWLEDGE),
    }

    app.track_title = music.get_current_track(gs)
    new_labels = [option["label"] for option in options]

    if app.root.ids.activity_list.items != new_labels:
        app.root.ids.activity_list.items = new_labels


def check_button_pressed():
    return app.root.ids.button.state == "down" or app.key_enter_pressed


async def on_finish():
    display("--- GAME FINISHED ---")
    app.root.ids.button.text = "Игра окончена"


async def _wait_for_event(widget, event_name):
    future = asyncio.get_running_loop().create_future()

    def on_event(*_args):
        if not future.done():
            future.set_result(True)

    bind_kwargs = {event_name: on_event}
    widget.bind(**bind_kwargs)

    try:
        return await future
    finally:
        widget.unbind(**bind_kwargs)
