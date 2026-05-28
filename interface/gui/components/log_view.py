from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import (
    StringProperty,
    NumericProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from gameplay.api import formatters
from interface.gui.components.mixins import ColoredWidget

BADGE_WIDTH = dp(60)
ENTRY_PADDING_HORIZONTAL = dp(10)
ENTRY_PADDING_VERTICAL = dp(15)


class LogBody(RecycleDataViewBehavior, BoxLayout, ColoredWidget):
    entry_text = StringProperty("")
    badge_text = StringProperty("")
    font_size = NumericProperty()

    def refresh_view_attrs(self, rv, index, data):
        super().refresh_view_attrs(rv, index, data)

        self.entry_text = data.get("text", "")
        self.font_size = rv.font_size
        dt = data.get("dt", None)
        if dt is not None:
            self.badge_text = formatters.get_formatted_time(dt)
        else:
            self.badge_text = ""


class LogView(RecycleView, ColoredWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self._recalc_event = None
        self._last_width = 0
        self._calc_label = None
        Window.bind(on_resize=self.on_window_resize)
        Clock.schedule_once(self._init_calc_label, 0)

    def _init_calc_label(self, _dt):
        self._calc_label = CoreLabel(font_name="UMTypewriter", font_size=self.font_size)
        self.on_window_resize()

    def on_font_size(self, *_args):
        if self._calc_label:
            self._calc_label.font_size = self.font_size
            self._calc_label.refresh()
            self.on_window_resize()

    def _get_height(self, text, width):
        self._calc_label.text = text
        self._calc_label.text_size = (
            width - BADGE_WIDTH - ENTRY_PADDING_HORIZONTAL,
            None,
        )
        self._calc_label.refresh()
        height = self._calc_label.texture.size[1] + ENTRY_PADDING_VERTICAL
        return height

    BUFFER = 10

    def on_window_resize(self, *_args):
        if self.width <= 0 or not self.data:
            return

        if self._recalc_event and self._last_width != self.width:
            self._last_width = self.width
            self._recalc_event.cancel()

        indices = list(self.layout_manager.view_indices.values())
        if not indices:
            return

        start_idx = max(0, min(indices) - self.BUFFER)
        end_idx = min(len(self.data) - 1, max(indices) + self.BUFFER)

        visible = range(start_idx, end_idx + 1)
        others = [i for i in range(len(self.data)) if i not in visible]
        queue = list(visible) + others

        self._recalc_event = Clock.schedule_once(
            lambda dt: self._process_recalc(self.width, queue, len(visible)), 0.05
        )

    CHUNK_SIZE = 300

    def _process_recalc(self, width, queue: list[int], chunk_size):
        chunk = queue[:chunk_size]

        for i in chunk:
            item = self.data[i]
            item["size"] = (width, self._get_height(item["text"], width))

        remaining = queue[chunk_size:]

        if chunk_size < self.CHUNK_SIZE or not remaining:
            self.refresh_from_data()

        if remaining:
            self._recalc_event = Clock.schedule_once(
                lambda dt: self._process_recalc(width, remaining, self.CHUNK_SIZE), 0.05
            )
        else:
            self._recalc_event = None

    def add_line(self, text, dt=None):
        height = self._get_height(text, self.width)
        self.data.append({"text": text, "dt": dt, "size": (self.width, height)})

        if self.ids.container.height + dp(50) > self.height:
            self.scroll_y = 0

    def get_clean_data(self) -> list[dict]:
        return [{"text": item["text"], "dt": item["dt"]} for item in self.data]

    def load_clean_data(self, history: list[dict]):
        if not history:
            return

        self.data = []
        for item in history:
            self.data.append(
                {"text": item["text"], "dt": item["dt"], "size": (self.width, dp(40))}
            )

        Clock.schedule_once(lambda _: self.on_window_resize(), 0)


class LogEntry(Label, ColoredWidget):
    p = ENTRY_PADDING_HORIZONTAL


class TimeBadge(Label, ColoredWidget):
    w = BADGE_WIDTH
