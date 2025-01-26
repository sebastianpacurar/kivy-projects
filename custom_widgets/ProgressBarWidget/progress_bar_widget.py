from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ColorProperty


class ProgressBarWidget(Widget):
    bars_color = ColorProperty([2, 153, 139, 255])
    max = NumericProperty(100)
    value = NumericProperty(0)
