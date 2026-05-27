from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from interface.gui.components.mixins import ColoredWidget


class StyledLabel(Label, ColoredWidget):
    pass


class StyledBoxLayout(BoxLayout, ColoredWidget):
    pass


class ImageButton(ButtonBehavior, BoxLayout, ColoredWidget):
    icon_source = StringProperty("")
