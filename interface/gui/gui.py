import asyncio

from kivy.app import App

from engine.schema import ActivityOptions, GameState
from gameplay.api import vitals, stats, time


class AppProxy:
    def __getattr__(self, name):
        return getattr(App.get_running_app(), name)

    def __setattr__(self, name, value):
        setattr(App.get_running_app(), name, value)


app = AppProxy()


def display(*message, sep: str = " "):

    message = sep.join(map(str, message))
    app.root.ids.logger.add_line(message)


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


def check_button_pressed():
    return app.root.ids.button.state == "down" or app.key_enter_pressed


def refresh_stats(gs: GameState, options: ActivityOptions):
    app.stats = {
        "time": f"{time.get_hour(gs):02}:{time.get_minute(gs):02}",
        "fatigue": vitals.get(gs, vitals.fatigue),
        "money": stats.get(gs, stats.money),
        "social": stats.get(gs, stats.social),
        "mental": vitals.get(gs, vitals.mental),
        "knowledge": stats.get(gs, stats.knowledge),
    }

    new_labels = [option["label"] for option in options]
    if app.root.ids.activity_list.items != new_labels:
        app.root.ids.activity_list.items = new_labels


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
