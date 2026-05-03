import asyncio

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import DictProperty, BooleanProperty

from interface import ui


class GameApp(App):
    stats = DictProperty(
        {
            "time": "undefined",
            "fatigue": 0,
            "money": 0,
            "social": 0,
            "mental": 0,
            "knowledge": 0,
        }
    )

    key_enter_pressed = BooleanProperty(False)

    def __init__(self, gs, get_options_func, **kwargs):
        super().__init__(**kwargs)
        self.gs = gs
        self.get_options_func = get_options_func
        self.activity_options = []
        self.ready = asyncio.Future()

    def build(self):
        return Builder.load_file("interface/gui/style.kv")

    def on_start(self):
        Window.bind(on_key_down=self._on_key_down)
        Window.bind(on_key_up=self._on_key_up)

        self.ready.set_result(True)

        def update(_):
            ui.refresh_stats(self.gs, self.get_options_func())

        Clock.schedule_interval(update, 1 / 60)

    def on_stats(self, _, value):
        self.root.ids.info.text = (
            f"time: {value['time']}\n"
            f"fatigue: {value['fatigue']}   money: {value['money']}   social: {value['social']}   "
            f"mental: {value['mental']}   knowledge: {value['knowledge']}"
        )

    def _on_key_down(self, _window, key, *_args):
        if key == 13:
            self.key_enter_pressed = True
            self.root.ids.button.dispatch("on_press")

    def _on_key_up(self, _window, key, *_args):
        if key == 13:
            self.key_enter_pressed = False
