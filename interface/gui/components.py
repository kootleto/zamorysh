from kivy.properties import (
    ListProperty,
    NumericProperty,
)
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton


class ListButton(ToggleButton):
    pass


class SelectableList(ScrollView):
    items = ListProperty([])
    selected_index = NumericProperty(-1)

    def on_items(self, _, value):
        self.ids.container.clear_widgets()

        for i, text in enumerate(value):
            btn = ListButton(text=text, group="list")
            btn.index = i
            btn.bind(state=self.on_state_change)
            self.ids.container.add_widget(btn)

    def on_state_change(self, btn, _):
        if btn.state == "down":
            self.selected_index = btn.index

    def on_selected_index(self, _, value):
        if value == -1:
            for btn in self.ids.container.children:
                if isinstance(btn, ListButton):
                    btn.state = "normal"


class LogView(ScrollView):
    def add_line(self, text):
        lbl = LogLabel(text=text)
        self.ids.container.add_widget(lbl)
        if self.ids.container.height > self.height:
            self.scroll_y = 0


class LogLabel(Label):
    pass
