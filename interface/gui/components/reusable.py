from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from interface.gui.components.mixins import ColoredWidget


class StyledLabel(Label, ColoredWidget):
    pass


class StyledBoxLayout(BoxLayout, ColoredWidget):
    pass
