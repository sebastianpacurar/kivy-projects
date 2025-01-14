from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


class BaseButton(Button):
    min_width = NumericProperty(dp(100))

    def on_kv_post(self, base_widget):
        if self.parent and self.parent.width > self.min_width:
            self.min_width = self.parent.width - dp(20)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                return super(Button, self).on_touch_down(touch)
            if touch.button == 'right':
                return False


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
    bg_color = ListProperty([1, 1, 1, 0])  # default to transparent

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
