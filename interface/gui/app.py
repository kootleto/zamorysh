import asyncio
import os.path

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import DictProperty, BooleanProperty, StringProperty

from engine.schema import GameState
from interface import ui
from interface.gui.gui import KivyState


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
    track_title = StringProperty(None)

    key_enter_pressed = BooleanProperty(False)

    def __init__(self, gs: GameState, vs: KivyState, get_options_func, **kwargs):
        super().__init__(**kwargs)
        self.gs = gs
        self.vs = vs
        self.get_options_func = get_options_func
        self.track_source = None
        self.activity_options = []
        self.ready = asyncio.Future()

    def build(self):
        return Builder.load_file("interface/gui/style.kv")

    def on_start(self):
        Window.bind(on_key_down=self._on_key_down)
        Window.bind(on_key_up=self._on_key_up)

        self.ready.set_result(True)

        def update(_):
            ui.refresh_ui(self.gs, self.vs, self.get_options_func())

        Clock.schedule_interval(update, 1 / 60)

    def on_stats(self, _, value):
        self.root.ids.info.text = (
            f"time: {value['time']}\n"
            f"fatigue: {value['fatigue']}   money: {value['money']}   social: {value['social']}   "
            f"mental: {value['mental']}   knowledge: {value['knowledge']}"
        )

    def on_track_title(self, _, value):
        if self.track_source:
            self.track_source.stop()
            self.track_source.unload()
            self.track_source = None

        if not value:
            return

        path = f"assets/music/{value}.wav"
        if not os.path.exists(path):
            raise FileNotFoundError(f"File '{path}' not found")

        self.track_source = SoundLoader.load(path)
        self.track_source.loop = True
        self.track_source.volume = self.vs["volume"] / 100
        Clock.schedule_once(lambda *args: self.track_source.play(), 0.1)

    def _on_key_down(self, _window, key, *_args):
        if key == 13:
            self.key_enter_pressed = True
            self.root.ids.button.dispatch("on_press")

    def _on_key_up(self, _window, key, *_args):
        if key == 13:
            self.key_enter_pressed = False
