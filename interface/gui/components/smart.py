import asyncio

from kivy.graphics import Rectangle, Color, Ellipse
from kivy.metrics import sp, dp
from kivy.properties import (
    ListProperty,
    NumericProperty,
)
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton

from interface.gui.components.mixins import ColoredWidget, CoverImage


class GameButton(Button):
    pass


class MenuItem(ToggleButton):

    def on_touch_up(self, touch):
        if touch.grab_current is self and not self.collide_point(*touch.pos):
            touch.ungrab(self)
            self.state = "normal"
            return True

        return super().on_touch_up(touch)


class Menu(ScrollView, ColoredWidget):
    items = ListProperty([])
    selected_index = NumericProperty(-1)
    font_size = NumericProperty()
    _selection_future = None
    awaits_selection = False

    def on_items(self, _, value):
        self.ids.container.clear_widgets()

        for i, text in enumerate(value):
            btn = MenuItem(text=text, group="list")
            btn.index = i
            btn.bind(on_release=self.on_item_release)
            self.ids.container.add_widget(btn)

    def on_font_size(self, _, value):
        for btn in self.ids.container.children:
            btn.font_size = value

    async def wait_selection(self):
        self._selection_future = asyncio.get_running_loop().create_future()
        return await self._selection_future

    def on_item_release(self, _btn):
        group_list = ToggleButtonBehavior.get_widgets("list")
        down_buttons = [b for b in group_list if b.state == "down"]
        self.selected_index = down_buttons[0].index if down_buttons else -1

    def on_selected_index(self, _, value):
        if self._selection_future and not self._selection_future.done():
            self._selection_future.set_result(value)

    def reset_selection(self):
        self.selected_index = -1
        for btn in ToggleButtonBehavior.get_widgets("list"):
            btn.state = "normal"


class VolumeSlider(Slider):
    track_color = ListProperty()
    cursor_color = ListProperty()
    track_height = NumericProperty()
    custom_cursor_size = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_width = 0
        self.cursor_image = ""
        self.cursor_size = (0, 0)

        with self.canvas.before:
            self.graphics_color = Color()
            self.track_rect = Rectangle()

        with self.canvas.after:
            self.circle_color = Color()
            self.circle = Ellipse()

        self.bind(
            pos=self._update_track,
            size=self._update_track,
            track_color=self._update_track,
            value_pos=self._update_circle,
            cursor_color=self._update_circle,
        )

    def _update_track(self, *_args):
        if self.track_color:
            self.graphics_color.rgba = self.track_color

        track_length = self.width - dp(20)
        self.track_rect.size = (track_length, self.track_height)
        self.track_rect.pos = (
            self.center_x - track_length / 2,
            self.center_y - self.track_height / 2,
        )

    def _update_circle(self, *_args):
        if self.circle_color:
            self.circle_color.rgba = self.cursor_color

        self.circle.size = (self.custom_cursor_size, self.custom_cursor_size)
        self.circle.pos = (
            self.value_pos[0] - self.custom_cursor_size / 2,
            self.center_y - self.custom_cursor_size / 2,
        )


class SceneView(BoxLayout, ColoredWidget):
    pass


class StatLabel(BoxLayout):
    pass


class MainScreen(BoxLayout, CoverImage):
    unit = NumericProperty(1)
    space_nano = NumericProperty()
    space_sm = NumericProperty()
    space_1 = NumericProperty()
    space_2 = NumericProperty()
    space_3 = NumericProperty()
    space_4 = NumericProperty()

    text_nano = NumericProperty()
    text_sm = NumericProperty()
    text_md = NumericProperty()
    text_lg = NumericProperty()
    text_xl = NumericProperty()

    def on_size(self, *_args):
        self.unit = self.width / 1000

        self.space_nano = self.unit
        self.space_sm = self.unit * 3
        self.space_1 = self.unit * 5
        self.space_2 = self.unit * 10
        self.space_3 = self.unit * 15
        self.space_4 = self.unit * 20

        if self.width < 600:
            base = sp(14)  # Телефон
        elif self.width < 1000:
            base = sp(16)  # Планшет
        else:
            base = sp(18)  # Десктоп

        self.text_nano = base * 0.7
        self.text_sm = base * 0.8
        self.text_md = base
        self.text_lg = base * 1.3
        self.text_xl = base * 1.8
