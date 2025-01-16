from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

from custom_components.BaseComponents.base_components import PropCachedWidget
from utils import rgb_format


class IconButton(ButtonBehavior, BoxLayout, PropCachedWidget):
    icon = StringProperty('')  # icon unicode
    primary_state_color = ListProperty(rgb_format([2, 153, 139, 255]))  # defaults to Teal
    secondary_state_color = ListProperty(rgb_format([200, 0, 0, 255]))  # defaults to Reddish
    bg_color = ListProperty([])  # listener for color changing events
    is_round = ListProperty([1, 1, 1, 1])  # using explicit rounded borders
    is_secondary_state = BooleanProperty(False)  # change color to secondary_state_color if is_secondary_state is True
    label_text = StringProperty('')  # button label text. if empty, it's just an icon button, else labeled icon button
    bg_size_val = NumericProperty(dp(36))  # used with font_size_val to get different sized icons
    font_size_val = NumericProperty(sp(28))  # if no text label, this should be of the size of the bg_size_val
    x_padding = NumericProperty(dp(24))  # if no text, this should be 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_hovered = False  # track hover state
        self.primary_state_pressed = rgb_format(self.primary_state_color, 0.25, lighten=True)
        self.primary_state_hovered = rgb_format(self.primary_state_color, 0.25, darken=True)
        self.secondary_state_pressed = rgb_format(self.secondary_state_color, 0.25, lighten=True)
        self.secondary_state_hovered = rgb_format(self.secondary_state_color, 0.25, darken=True)
        self.disabled_state_color = rgb_format([255, 255, 255, 255], factor=0.4, darken=True)
        self.bg_color = self.primary_state_color  # listener for canvas updates (actual color of the displayed canvas)

        self.bind(size=self.update_canvas, pos=self.update_canvas)
        self.bind(bg_color=self.update_canvas)
        self.bind(state=self.on_state, is_secondary_state=self.on_state)  # bind the state property to the on_state method
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.setup_initialized = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                # if left click, proceed with the button press logic
                return super(IconButton, self).on_touch_down(touch)
            if touch.button == 'right':
                # do nothing if right click
                return False

    def on_icon(self, instance, value):
        """ Set text to the Unicode value when the icon is assigned \n
            Set sizing and positioning for label when first runs
        """
        Clock.schedule_once(lambda dt: self.delayed_setup(value), .1)

    def delayed_setup(self, value):
        self.ids.icon_label.text = value  # set unicode icon
        if not self.setup_initialized:
            # if empty string, format icon to be placed in the middle
            if len(self.label_text) == 0:
                # remove all spacing and padding. set font_size_val ref to bg_size_val
                self.x_padding = 0
                self.padding = [0, 0, 0, dp(1)]
                self.ids.icon_label.font_size = self.bg_size_val
                self.remove_widget(self.ids.space_filler)
                self.remove_widget(self.ids.text_label)
                self.setup_initialized = True
                self.width = self.bg_size_val
            else:
                self.width = self.ids.text_label.width + self.ids.icon_label.font_size + self.x_padding

            self.cached_props = {
                'bg_size_val': {'displayed': self.bg_size_val, 'hidden': 0},
                'font_size_val': {'displayed': self.font_size_val, 'hidden': 0},
                'x_padding': {'displayed': self.x_padding, 'hidden': 0},
            }

    def update_bg_color(self):
        """ Update the background color based on the current state """
        if self.disabled:
            self.bg_color = self.disabled_state_color
        elif self.is_secondary_state:
            if self.state == 'down':
                self.bg_color = self.secondary_state_pressed
            elif self.is_hovered:
                self.bg_color = self.secondary_state_hovered
            else:
                self.bg_color = self.secondary_state_color
        else:
            if self.state == 'down':
                self.bg_color = self.primary_state_pressed
            elif self.is_hovered:
                self.bg_color = self.primary_state_hovered
            else:
                self.bg_color = self.primary_state_color

    def on_mouse_pos(self, window, pos):
        """ Check if mouse hovers over the button """
        is_now_hovered = self.collide_point(*self.to_widget(*pos))
        if is_now_hovered != self.is_hovered:
            self.is_hovered = is_now_hovered
            self.update_bg_color()
            self.update_canvas()

    def on_state(self, instance, value):
        """ Set background color based on the state ('down' or 'normal') of the button """
        self.update_bg_color()
        self.update_canvas()

    def on_disabled(self, instance, value):
        """ Update background color when the button is disabled """
        self.update_bg_color()
        self.update_canvas()

    def update_canvas(self, *args):
        """ Update the background color and rectangle to match a button's behavior """
        self.canvas.before.clear()
        with self.canvas.before:  # redraw with bg_color values
            Color(*self.bg_color)
            if any(self.is_round):
                self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[
                    self.is_round[0] * self.height / 4,  # top-left
                    self.is_round[1] * self.height / 4,  # top-right
                    self.is_round[2] * self.height / 4,  # bottom-left
                    self.is_round[3] * self.height / 4,  # bottom-right
                ])
            else:  # use Rectangle for no rounding
                self.rect = Rectangle(size=self.size, pos=self.pos)

    def hide_widget(self, props=None):
        super().hide_widget(self.cached_props)

    def reveal_widget(self, props=None):
        super().reveal_widget()
