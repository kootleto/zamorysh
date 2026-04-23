import asyncio
import os
import traceback

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import DictProperty

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

    def __init__(self, gs, **kwargs):
        super().__init__(**kwargs)
        self.gs = gs
        self.ready = asyncio.Future()

    def build(self):
        print("STYLE LOADING STARTED")
        try:
            current_dir = os.path.dirname(__file__)
            kv_path = os.path.join(current_dir, "style.kv")
            root = Builder.load_file(kv_path)
            return root
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            print("STYLE LOADING FINISHED")

    def on_start(self):
        self.ready.set_result(True)

        def update(_):
            ui.refresh_stats(self.gs)

        Clock.schedule_interval(update, 1 / 60)

    def on_stats(self, _, value):
        self.root.ids.info.text = (
            f"time: {value['time']}\n"
            f"fatigue: {value['fatigue']}   money: {value['money']}   social: {value['social']}   "
            f"mental: {value['mental']}   knowledge: {value['knowledge']}"
        )
