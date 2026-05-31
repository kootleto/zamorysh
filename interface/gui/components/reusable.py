from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from interface.gui.components.mixins import ColoredWidget


class StyledLabel(Label, ColoredWidget):
    pass


class StyledBoxLayout(BoxLayout, ColoredWidget):
    pass


class ImageButton(Button):
    icon_source = StringProperty("")
