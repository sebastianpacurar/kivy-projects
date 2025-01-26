from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.properties import ListProperty, BooleanProperty, ColorProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from utils import rgb_format


class PropCachedWidget(Widget):
    """ Base class to handle hide and display when using fixed sizes """
    cached_props = {}

    def on_kv_post(self, base_widget):
        self.cached_props = {
            'size': {'displayed': tuple(self.size), 'hidden': (0, 0)},
            'size_hint': {'displayed': tuple(self.size_hint), 'hidden': (None, None)},
            'opacity': {'displayed': 1, 'hidden': 0},
            'disabled': {'displayed': 0, 'hidden': 1}
        }

    def hide_widget(self, props=None):
        """ Hide the widget """
        for prop, values in self.cached_props.items():
            hidden_value = values['hidden']
            setattr(self, prop, hidden_value)

    def reveal_widget(self):
        """ Restore the widget by setting all ca"""
        for prop in self.cached_props:
            cached_values = self.cached_props.get(prop)
            if cached_values:
                displayed_value = cached_values['displayed']
                setattr(self, prop, displayed_value)

    def recursive_hide(self, widget):
        """ Hide children recursively"""
        for child in widget.children:
            if isinstance(child, PropCachedWidget):
                child.hide_widget()
            self.recursive_hide(child)

    def recursive_reveal(self, widget):
        """ Reveal hidden children recursively"""
        for child in widget.children:
            if isinstance(child, PropCachedWidget):
                child.reveal_widget()
            self.recursive_reveal(child)


class BaseLabel(Label, PropCachedWidget):
    bg_color = ColorProperty([1, 1, 1, 0])  # default to transparent

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.cached_props = {**self.cached_props, **{
            'font_size': {'displayed': self.font_size, 'hidden': 0}
        }}

    def hide_widget(self, props=None):
        super().hide_widget(self.cached_props)

    def reveal_widget(self):
        super().reveal_widget()


class BaseTextInput(TextInput, PropCachedWidget):
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.cached_props = {**self.cached_props, **{
            'padding': {'displayed': self.padding.copy(), 'hidden': [0, 0, 0, 0]},
            'font_size': {'displayed': self.font_size, 'hidden': 0}
        }}

    def hide_widget(self, props=None):
        super().hide_widget(self.cached_props)

    def reveal_widget(self):
        super().reveal_widget()


class TextLabel(BaseLabel):
    # TextLabel is based on BaseLabel which is already a PropCachedWidget
    pass


# currently used by SimpleButton and IconButton
class BaseButtonBehavior(ButtonBehavior, BoxLayout):
    primary_state_color = ColorProperty(rgb_format([2, 153, 139, 255]))  # defaults to Teal
    secondary_state_color = ColorProperty(rgb_format([200, 0, 0, 255]))  # defaults to Reddish
    bg_color = ColorProperty([0, 0, 0, 1])  # listener for color changing events
    roundness = ListProperty([1, 1, 1, 1])  # using explicit rounded borders
    is_secondary_state = BooleanProperty(False)  # change color to secondary_state_color if is_secondary_state is True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_hovered = False
        self.primary_state_pressed = rgb_format(self.primary_state_color, 0.3, darken=True)
        self.primary_state_hovered = rgb_format(self.primary_state_color, 0.2, lighten=True)
        self.secondary_state_pressed = rgb_format(self.secondary_state_color, 0.3, darken=True)
        self.secondary_state_hovered = rgb_format(self.secondary_state_color, 0.2, lighten=True)
        self.disabled_state_color = rgb_format([255, 255, 255, 255], factor=0.4, darken=True)

        self.bg_color = self.primary_state_color
        self.bind(size=self.update_canvas, pos=self.update_canvas, bg_color=self.update_canvas)
        self.bind(state=self.on_state, is_secondary_state=self.on_state)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_primary_state_color(self, instance, value):
        self.primary_state_pressed = rgb_format(value, 0.25, lighten=True)
        self.primary_state_hovered = rgb_format(value, 0.25, darken=True)
        self.bg_color = self.primary_state_color

    def on_secondary_state_color(self, instance, value):
        self.secondary_state_pressed = rgb_format(value, 0.25, lighten=True)
        self.secondary_state_hovered = rgb_format(value, 0.25, darken=True)
        self.bg_color = self.secondary_state_color

    def on_touch_down(self, touch):
        """Trigger ripple on touch."""
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                return super().on_touch_down(touch)
            return False

    def update_bg_color(self):
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

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            if any(self.roundness):
                self.rect = RoundedRectangle(
                    size=self.size,
                    pos=self.pos,
                    radius=[self.roundness[0] * self.height / 4,
                            self.roundness[1] * self.height / 4,
                            self.roundness[2] * self.height / 4,
                            self.roundness[3] * self.height / 4]
                )
            else:
                self.rect = Rectangle(size=self.size, pos=self.pos)

    def on_mouse_pos(self, window, pos):
        local_pos = self.to_widget(*pos)
        is_now_hovered = self.collide_point(*local_pos)
        if is_now_hovered != self.is_hovered:
            self.is_hovered = is_now_hovered
            self.update_bg_color()
            self.update_canvas()

    def on_state(self, instance, value):
        self.update_bg_color()
        self.update_canvas()

    def on_disabled(self, instance, value):
        self.update_bg_color()
        self.update_canvas()
