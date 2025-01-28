from kivy.metrics import dp
from kivy.properties import BoundedNumericProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from utils import generate_color
from custom_widgets.base_widgets import BaseLabel


class ColorPickerWidget(BoxLayout):
    red = BoundedNumericProperty(0, min=0, max=255)
    green = BoundedNumericProperty(0, min=0, max=255)
    blue = BoundedNumericProperty(0, min=0, max=255)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_slider_value_change(self, color, value):
        setattr(self, color, int(value))

    def set_color_from_table(self, value):
        for i, color in enumerate([self.ids.red_slider, self.ids.green_slider, self.ids.blue_slider]):
            color.value = int(value[i] * 255)


class ColorTable(BoxLayout):
    def on_kv_post(self, touch):
        lightened = ColorGrid(orientation='rl-tb')
        darkened = ColorGrid(orientation='lr-tb')
        self.add_widget(lightened)
        self.add_widget(darkened)
        self.height = lightened.height
        self.width = lightened.width + darkened.width


class ColorGrid(GridLayout):
    cols = NumericProperty(15)
    rows = NumericProperty(15)
    cell_size = NumericProperty(dp(15))
    min_b = NumericProperty(0.1)
    max_b = NumericProperty(1.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = self.cell_size * self.cols
        self.width = self.cell_size * self.rows

    def on_kv_post(self, base_widget):
        self.is_first, self.is_last = None, None
        self.create_grid()

    def create_grid(self):
        """ Create the grid based on brightness level """
        for col in range(self.cols):
            r, g, b = generate_color(col / self.cols)

            # from brightest to darkest
            for row in range(self.rows):
                brightness_factor = 1 - (row / (self.rows - 1))  # brightness factor transitioning from max to min
                adjusted_brightness = self.min_b + (self.max_b - self.min_b) * brightness_factor  # set brightness based on row and clamp between min and max

                if self.orientation == 'lr-tb':
                    # darken
                    r_bright = r * adjusted_brightness
                    g_bright = g * adjusted_brightness
                    b_bright = b * adjusted_brightness
                    self.is_first = row == self.rows - 1
                else:
                    # lighten
                    r_bright = r * adjusted_brightness + (1 - adjusted_brightness)
                    g_bright = g * adjusted_brightness + (1 - adjusted_brightness)
                    b_bright = b * adjusted_brightness + (1 - adjusted_brightness)
                    self.is_last = row == 0
                    self.is_first = row == self.rows - 1

                # hide first and last columns for left grid, and hide last row for right grid
                condition = False
                if self.is_last is not None:
                    condition = self.is_last and self.is_last
                else:
                    condition = self.is_first

                color_box = ColorBox(
                    bg_color=[r_bright, g_bright, b_bright, 1],
                    size=(self.cell_size, self.cell_size),
                    opacity=0 if condition else 1,
                    disabled=1 if condition else 0
                )
                self.add_widget(color_box)


class ColorBox(BaseLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None

    def on_touch_down(self, touch):
        if not self.disabled:
            if self.collide_point(*touch.pos):
                self.set_sliders_color()
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if not self.disabled:
            if self.collide_point(*touch.pos):
                self.set_sliders_color()
        return super().on_touch_move(touch)

    def set_sliders_color(self):
        parent = self.parent
        while parent:
            if hasattr(parent, 'set_color_from_table'):
                parent.set_color_from_table(self.bg_color)
                break
            parent = parent.parent
