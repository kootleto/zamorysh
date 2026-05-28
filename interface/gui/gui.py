import asyncio
from copy import deepcopy
from typing import TypedDict, Callable

from kivy.app import App

from engine.schema import ActivityOptions, GameState
from gameplay.api import vitals, stats, time, music, location, scene, formatters
from tools import storage
from tools.utils import ensure_callable


class AppProxy:
    def __getattr__(self, name):
        return getattr(App.get_running_app(), name)

    def __setattr__(self, name, value):
        setattr(App.get_running_app(), name, value)


app = AppProxy()


class KivyState(TypedDict):
    volume: int
    fullscreen: bool
    muted: bool
    log_history: list


INITIAL_UI_STATE: KivyState = {
    "volume": 100,
    "fullscreen": True,
    "muted": True,
    "log_history": [],
}


def init_ui(vs_path) -> KivyState:
    vs = storage.read_data(vs_path)
    return vs if vs else deepcopy(INITIAL_UI_STATE)


def display(*message, sep: str = " "):

    message = sep.join(map(str, message))
    app.root.ids.logger.add_line(message)


def display_at(gs, *message, sep: str = " "):
    dt = time.get_datetime(gs)
    message = sep.join(map(str, message))
    app.root.ids.logger.add_line(message, dt=dt)


# DEPRECATED
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


async def ask_option(
    options,
    message,
    submit_required=False,
    submit_message: str | Callable[[int], str] | None = None,
    cols=3,
):
    menu = app.root.ids.menu
    button = app.root.ids.button

    button.text = message
    menu.awaits_selection = True
    menu.reset_selection()
    menu.items = [str(option) for option in options]
    menu.cols = cols

    selected = await menu.wait_selection()
    if submit_required:
        while True:
            if selected != -1:
                button.text = ensure_callable(submit_message)(selected)
            else:
                button.text = message

            task_change = asyncio.create_task(menu.wait_selection())
            task_submit = asyncio.create_task(_wait_for_event(button, "on_press"))

            done, pending = await asyncio.wait(
                [task_change, task_submit], return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()

            if task_submit in done and selected != -1:
                break

            if task_change in done:
                selected = task_change.result()

    menu.reset_selection()
    menu.awaits_selection = False
    return options[selected]


async def prompt_activity(options: ActivityOptions) -> int:
    app.system_buttons_active = True

    def get_submit_message(idx):
        if options[idx]["hold_required"]:
            return "Нажмите и удерживайте"
        else:
            return "Нажмите на кнопку"

    labels = [option["label"] for option in options]
    selected = labels.index(
        await ask_option(
            labels,
            "Выберите активность",
            submit_required=True,
            submit_message=get_submit_message,
            cols=2,
        )
    )

    app.system_buttons_active = False

    return selected


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
    app.scene_name = scene.get_current_scene(gs)
    app.sprite_name = scene.get_current_sprite(gs)
    new_labels = [option["label"] for option in options]

    if not app.root.ids.menu.awaits_selection:
        if app.root.ids.menu.items != new_labels:
            app.root.ids.menu.items = new_labels
        app.root.ids.button.text = formatters.get_formatted_time(app.stats["datetime"])


def check_button_pressed():
    return app.root.ids.button.state == "down" or app.key_enter_pressed


async def on_finish():
    response = await ask_option(
        ["Выйти", "Начать новую игру"], "Игра окончена.", cols=2
    )
    if response == "Выйти":
        app.session_result.set_result("exit")
    else:
        app.session_result.set_result("restart")


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
