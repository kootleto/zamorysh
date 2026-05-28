import asyncio
import os.path

from kivy import platform
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

import constants
from engine import controller
from engine.schema import GameState
from gameplay.api import formatters
from interface import ui
from interface.gui.gui import KivyState, INITIAL_UI_STATE
from tools import storage


class GameApp(App):
    title = "Zamorysh"
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
        }
    )
    track_title = StringProperty(None)
    scene_name = StringProperty(None)
    sprite_name = StringProperty(None)
    volume = NumericProperty(100)
    fullscreen = BooleanProperty(False)
    muted = BooleanProperty(False)
    key_enter_pressed = BooleanProperty(False)
    system_buttons_active = BooleanProperty(False)

    def __init__(
        self, gs: GameState, vs: KivyState, get_options_func, is_save, **kwargs
    ):
        super().__init__(**kwargs)
        self.gs = gs
        self.get_options_func = get_options_func
        self.activity_options = []
        self.ready = asyncio.Future()
        self.current_track = None
        self.volume = vs["volume"]
        self.fullscreen = vs["fullscreen"]
        self.muted = vs["muted"]
        self.log_history = (
            vs["log_history"] if is_save else INITIAL_UI_STATE["log_history"]
        )

    def build(self):
        Builder.unload_file("interface/gui/style.kv")
        return Builder.load_file("interface/gui/style.kv")

    def on_start(self):
        Window.bind(on_key_down=self._on_key_down)
        Window.bind(on_key_up=self._on_key_up)
        self.root.ids.logger.load_clean_data(self.log_history)

        def update(_):

            if App.get_running_app() is None:
                return False

            ui.refresh_ui(self.gs, self.get_options_func())
            return True

        Clock.schedule_interval(update, 1 / 60)
        Clock.schedule_once(lambda _: self.ready.set_result(True), 0)

        if platform == "android":
            box = self.root.ids.system_buttons_box
            btn = self.root.ids.fullscreen_button
            box.remove_widget(btn)

    def on_stats(self, _, value):
        self.root.ids.money_stat_label.value = round(value["money"], 1)
        self.root.ids.knowledge_stat_label.value = round(value["knowledge"], 1)
        self.root.ids.social_stat_label.value = round(value["social"], 1)
        self.root.ids.time_label.text = formatters.get_formatted_time(value["datetime"])
        self.root.ids.date_label.text = formatters.get_formatted_date(value["datetime"])
        # TODO: remove that...
        # self.root.ids.map_label.text = (
        #     f"Location: {value["location"]["place"]}\nX: {value["location"]["x"]}, "
        #     f"Y: {value["location"]["y"]}"
        # )

    @staticmethod
    def _resolve_assets_path(filename, folder):
        path = folder + filename
        if not os.path.exists(path):
            raise FileNotFoundError(f"File '{path}' not found")
        return path

    def on_track_title(self, _, value):
        print("")
        if self.current_track:
            self.current_track.stop()
            self.current_track.unload()
            self.current_track = None

        if not value:
            return

        path = self._resolve_assets_path(value, "assets/music/")

        self.current_track = SoundLoader.load(path)
        if self.current_track:
            self.current_track.loop = True
            self.current_track.volume = 0 if self.muted else self.volume / 100
            self.current_track.play()

    def on_scene_name(self, _, value):
        path = self._resolve_assets_path(value, "assets/images/scenes/")
        self.root.ids.scene.bg = path

    def on_sprite_name(self, _, value):
        path = self._resolve_assets_path(value, "assets/images/sprites/")
        self.root.ids.scene.sprite = path

    def on_volume(self, _, value):
        if self.current_track and not self.muted:
            self.current_track.volume = value / 100

    @staticmethod
    def on_fullscreen(_, value):
        Window.fullscreen = "auto" if value else False

    def on_muted(self, _, value):
        volume_to = 0 if value else self.volume / 100
        if self.current_track:
            self.current_track.volume = volume_to

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

    def toggle_mute(self):
        self.muted = not self.muted

    def save_game(self):
        controller.save_game(self.gs, constants.GAME_STATE_PATH)
        ui.display_save_notification()

    session_result = None

    def exit_game(self):
        self.stop()
        self.session_result.set_result("exit")

    def _on_key_down(self, _window, key, *_args):
        if key == 13:
            self.key_enter_pressed = True
            self.root.ids.button.dispatch("on_press")

    def _on_key_up(self, _window, key, *_args):
        if key == 13:
            self.key_enter_pressed = False

    _saved_on_exit = False

    def on_stop(self):
        if self._saved_on_exit:
            return

        self._saved_on_exit = True

        controller.save_game(self.gs, constants.GAME_STATE_PATH)
        log_history = self.root.ids.logger.get_clean_data()
        vs: KivyState = {
            "volume": self.volume,
            "fullscreen": self.fullscreen,
            "muted": self.muted,
            "log_history": log_history,
        }
        storage.write_data(constants.VIEW_STATE_PATH, vs)

        if self.current_track:
            self.current_track.stop()
            self.current_track.unload()
