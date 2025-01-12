from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

from utils import rgb_format


class IconButton(ButtonBehavior, BoxLayout):
    icon = StringProperty('')  # icon unicode
    bg_color = ListProperty(rgb_format([2, 153, 139, 255]))  # listener for color changing events
    default_bg_color = rgb_format([2, 153, 139, 255])
    pressed_bg_color = rgb_format(default_bg_color, 0.25, lighten=True)
    hovered_bg_color = rgb_format(default_bg_color, 0.25, darken=True)
    red_state_default_bg_color = rgb_format([200, 0, 0, 255])
    red_state_pressed_bg_color = rgb_format(red_state_default_bg_color, 0.25, lighten=True)
    red_state_hovered_bg_color = rgb_format(red_state_default_bg_color, 0.25, darken=True)
    disabled_bg_color = rgb_format([255, 255, 255, 255], factor=0.4, darken=True)
    is_round = BooleanProperty(True)
    is_red_state = BooleanProperty(False)  # change color to red if is_red_state is True
    label_text = StringProperty('')  # button label text. if empty, it's just an icon button, else labeled icon button
    bg_size_val = NumericProperty(dp(36))  # used with font_size_val to get different sized icons
    font_size_val = NumericProperty(sp(28))  # if no text label, this should be of the size of the bg_size_val
    x_padding = NumericProperty(dp(24))  # if no text, this should be 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_hovered = False  # track hover state
        # make sure no other drawings are made while there is an animation or screen transition
        self.bind(size=self.update_canvas, pos=self.update_canvas)
        self.bind(bg_color=self.update_canvas)  # when bg_color changes, trigger canvas redraw
        self.bind(state=self.on_state, is_red_state=self.on_state)  # bind the state property to the on_state method
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
        # if empty string, format icon to be placed in the middle
        if len(self.label_text) == 0 and not self.setup_initialized:
            # remove all spacing and padding. set font_size_val ref to bg_size_val
            self.x_padding = 0
            self.padding = [0, 0, 0, dp(1)]
            self.ids.icon_label.font_size = self.bg_size_val
            self.remove_widget(self.ids.space_filler)
            self.remove_widget(self.ids.text_label)
            self.setup_initialized = True

    def update_bg_color(self):
        """ Update the background color based on the current state """
        if self.disabled:
            self.bg_color = self.disabled_bg_color
        elif self.is_red_state:
            if self.state == 'down':
                self.bg_color = self.red_state_pressed_bg_color
            elif self.is_hovered:
                self.bg_color = self.red_state_hovered_bg_color
            else:
                self.bg_color = self.red_state_default_bg_color
        else:
            if self.state == 'down':
                self.bg_color = self.pressed_bg_color
            elif self.is_hovered:
                self.bg_color = self.hovered_bg_color
            else:
                self.bg_color = self.default_bg_color

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
        self.canvas.before.clear()  # clear existent drawing
        with self.canvas.before:  # redraw with bg_color values
            Color(*self.bg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos) if self.is_round else Rectangle(size=self.size, pos=self.pos)
