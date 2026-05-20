import asyncio
import os.path

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (
    DictProperty,
    BooleanProperty,
    StringProperty,
    NumericProperty,
)

from engine.schema import GameState
from gameplay.api import formatters
from interface import ui
from interface.gui.gui import KivyState


class GameApp(App):
    stats = DictProperty(
        {
            "time": "undefined",
            "date": "undefined",
            "location": "undefined",
            "fatigue": 0,
            "money": 0,
            "social": 0,
            "mental": 0,
            "knowledge": 0,
            "location": None,
        }
    )
    track_title = StringProperty(None)
    volume = NumericProperty(100)

    key_enter_pressed = BooleanProperty(False)

    def __init__(self, gs: GameState, vs: KivyState, get_options_func, **kwargs):
        super().__init__(**kwargs)
        self.gs = gs
        self.vs = vs
        self.get_options_func = get_options_func
        self.activity_options = []
        self.ready = asyncio.Future()
        self.current_track = None

    def build(self):
        return Builder.load_file("interface/gui/style.kv")

    def on_start(self):
        Window.bind(on_key_down=self._on_key_down)
        Window.bind(on_key_up=self._on_key_up)

        self.ready.set_result(True)

        def update(_):
            ui.refresh_ui(self.gs, self.get_options_func())

        Clock.schedule_interval(update, 1 / 60)

    def on_stats(self, _, value):
        self.root.ids.stats_label.text = (
            f"fatigue: {value['fatigue']}   money: {value['money']}   social: {value['social']}   "
            f"mental: {value['mental']}   knowledge: {value['knowledge']}   location: {value["location"]}"
        )
        self.root.ids.time_label.text = formatters.get_formatted_time(value["datetime"])
        self.root.ids.date_label.text = formatters.get_formatted_date(value["datetime"])
        self.root.ids.map_label.text = (
            f"Location: {value["location"]["place"]}\nX: {value["location"]["x"]}, "
            f"Y: {value["location"]["y"]}"
        )

    def on_track_title(self, _, value):
        if self.current_track:
            self.current_track.stop()
            self.current_track.unload()
            self.current_track = None

        if not value:
            return

        path = f"assets/music/{value}"
        if not os.path.exists(path):
            raise FileNotFoundError(f"File '{path}' not found")

        self.current_track = SoundLoader.load(path)
        if self.current_track:
            self.current_track.loop = True
            self.current_track.volume = self.volume / 100
            self.current_track.play()

    def on_volume(self, _, value):
        if self.current_track:
            self.current_track.volume = value / 100

    def _on_key_down(self, _window, key, *_args):
        if key == 13:
            self.key_enter_pressed = True
            self.root.ids.button.dispatch("on_press")

    def _on_key_up(self, _window, key, *_args):
        if key == 13:
            self.key_enter_pressed = False

    def on_stop(self):
        if self.current_track:
            self.current_track.stop()
            self.current_track.unload()
