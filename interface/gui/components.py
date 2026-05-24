from kivy.properties import (
    ListProperty,
    NumericProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

# --- Mixins ---


class ColoredWidget(Widget):
    bg_color = ListProperty([0, 1, 0, 1])


class CoverImage(Image):
    pass


# --- Reusable ---


class MainScreen(BoxLayout, CoverImage):
    pass


class StyledLabel(Label, ColoredWidget):
    pass


# --- Smart ---


class ChoiceItem(ToggleButton):
    pass


class GameButton(Button):
    pass


class CommandInput(TextInput):
    pass


class ChoiceSelector(ScrollView, ColoredWidget):
    items = ListProperty([])
    selected_index = NumericProperty(-1)

    def on_items(self, _, value):
        self.ids.container.clear_widgets()

        for i, text in enumerate(value):
            btn = ChoiceItem(text=text, group="list")
            btn.index = i
            btn.bind(state=self.on_state_change)
            self.ids.container.add_widget(btn)

    def on_state_change(self, btn, _):
        if btn.state == "down":
            self.selected_index = btn.index

    def on_selected_index(self, _, value):
        if value == -1:
            for btn in self.ids.container.children:
                if isinstance(btn, ChoiceItem):
                    btn.state = "normal"


class LogView(ScrollView, ColoredWidget):
    def add_line(self, text):
        lbl = LogEntry(text=text)
        self.ids.container.add_widget(lbl)
        if self.ids.container.height > self.height:
            self.scroll_y = 0


class LogEntry(Label, ColoredWidget):
    pass


class VolumeSlider(Slider):
    pass


class SceneView(BoxLayout, ColoredWidget):
    pass
