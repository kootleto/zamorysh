from kivy.properties import ListProperty
from kivy.uix.image import Image
from kivy.uix.widget import Widget


class ColoredWidget(Widget):
    bg_color = ListProperty([0, 1, 0, 1])


class CoverImage(Image):
    pass
