from kivy.properties import BoundedNumericProperty, BooleanProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorWheel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from named_rgb_hex import css_4_colors


class ColorPickerScreen(Screen):
    data = ListProperty([])

    def on_kv_post(self, base_widget):
        self.set_data()
        self.ids.responsive_grid.ids.rv.data = self.data

    def set_data(self):
        self.data = [{'name': c['name'], 'rgb': c['rgb'], 'hex': c['hex']} for c in css_4_colors]


class ColorCardItem(FloatLayout):
    name = StringProperty('')
    rgb = ListProperty([0, 0, 0, 255])
    hex = StringProperty('')


class ColorPickerWidget(BoxLayout):
    red = BoundedNumericProperty(0, min=0, max=255)
    green = BoundedNumericProperty(0, min=0, max=255)
    blue = BoundedNumericProperty(0, min=0, max=255)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.ids.color_wheel.bind(on_color=self.set_color_from_wheel)

    def on_slider_value_change(self, color, value):
        setattr(self, color, int(value))

    def set_color_from_wheel(self, value):
        for i, color in enumerate([self.ids.red_slider, self.ids.green_slider, self.ids.blue_slider]):
            color.value = int(value[i] * 255)


class ColorWheelWidget(ColorWheel):
    can_lighten = BooleanProperty(False)  # start from max light
    can_darken = BooleanProperty(True)

    def on_color(self, instance, value):
        self.parent.parent.parent.parent.set_color_from_wheel(value)

    def update_lighten_darken_states(self, *args):
        self.can_lighten = self.sv_idx > 0
        self.can_darken = self.sv_idx < len(self.sv_s) - self._piece_divisions

    def lighten(self):
        """ Increase the brightness by decreasing  \n
            Same functionality as on_touch_move outwards the center
        """
        if self.can_lighten:
            self.sv_idx -= 1
            self.recolor_wheel()
            self.update_lighten_darken_states()

    def darken(self):
        """ Decrease the brightness by moving sv_idx to a darker value \n
            Same functionality as on_touch_move towards the center
        """
        if self.can_darken:
            self.sv_idx += 1
            self.recolor_wheel()
            self.update_lighten_darken_states()

    # cancel on_touch_move, since lighten and darken already take care of that
    def on_touch_move(self, touch):
        return False
