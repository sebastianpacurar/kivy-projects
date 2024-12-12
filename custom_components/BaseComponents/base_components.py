from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton


class BaseButton(Button):
    pass


class BaseLabel(Label):
    bg_color = ListProperty([1, 1, 1, 0])  # default to transparent


class TopBar(BoxLayout):
    project_name = StringProperty('')


class SimpleDropdown(Spinner):
    options = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(options=self.update_width)

    def update_width(self, *args):
        """ Update width based on the longest option in the dropdown """
        longest_option = max(self.options, key=len)  # find the longest option by character length
        # calculate the width of the longest option
        self.width = max(self.texture_size[0], len(longest_option) * dp(10))


class SegmentedButton(ToggleButton):
    option_index = NumericProperty(0)

