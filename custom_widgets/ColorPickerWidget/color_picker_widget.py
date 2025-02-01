from kivy.graphics import Color, Line
from kivy.metrics import dp
from kivy.properties import BoundedNumericProperty, NumericProperty, StringProperty, ReferenceListProperty, ColorProperty, ListProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from utils import generate_color
from custom_widgets.base_widgets import BaseLabel


class ColorPickerWidget(BoxLayout):
    red = BoundedNumericProperty(0, min=0, max=255)
    green = BoundedNumericProperty(0, min=0, max=255)
    blue = BoundedNumericProperty(0, min=0, max=255)
    rgb_colors = ReferenceListProperty(red, green, blue)
    hex_val = StringProperty('#000000')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.focused_color_box = None  # currently selected ColorBox from the ColorTable

    def on_kv_post(self, base_widget):
        self.bind(rgb_colors=self.rgb_to_hex)  # convert to hex when any of r,g or b changes
        # start from purple-like color
        self.red = 104
        self.green = 4
        self.blue = 150

    def update_color_channel(self, instance, value):
        setattr(self, instance.parent.target_prop_attribute, int(value))

    def set_slider_vals_from_table(self, value):
        for i, s in enumerate([self.ids.red_slider, self.ids.green_slider, self.ids.blue_slider]):
            s.ids.slider_w.value = int(value[i] * 255)

    def rgb_to_hex(self, instance, value):
        self.hex_val = '#{:02X}{:02X}{:02X}'.format(self.red, self.green, self.blue)

    # update the focused_color_box transparency value when rgb_colors change
    def on_rgb_colors(self, instance, value):
        val = tuple(value)
        # set opacity to 0 for any displayed ColorBox border and clear the focused_color_box ref
        if self.focused_color_box is not None:
            self.focused_color_box.color_box_selection_color[-1] = 0
            self.focused_color_box = None

        # if the rgb val matches any ColorBox bg_color from the color_table, then focus it and set opacity to 1
        if val in self.color_table.color_boxes:
            self.focused_color_box = self.color_table.color_boxes[val]
            self.focused_color_box.color_box_selection_color[-1] = 1

    def hex_to_rgb(self, instance, value):
        hex_stripped = value[1:]
        # convert every 2 characters of hex in int base 16
        return [int(hex_stripped[i:i + 2], 16) for i in (0, 2, 4)]


class ColorTable(BoxLayout):
    color_boxes = DictProperty({})  # store all color BaseLabel widgets, in this form {rgb_value: widget}

    def on_kv_post(self, touch):
        lightened = ColorGrid(orientation='rl-tb')
        darkened = ColorGrid(orientation='lr-tb')
        self.add_widget(lightened)
        self.add_widget(darkened)
        self.height = lightened.height
        self.width = lightened.width + darkened.width
        self.color_boxes = {**lightened.color_boxes, **darkened.color_boxes}


class ColorGrid(GridLayout):
    cols = NumericProperty(15)
    rows = NumericProperty(15)
    cell_size = NumericProperty(dp(10))
    min_b = NumericProperty(0.1)
    max_b = NumericProperty(1.0)
    color_boxes = DictProperty({})

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

                # hide first and last columns for left grid, and hide last column (from rght to left) for right grid
                condition = False
                if self.is_last is not None:
                    condition = self.is_last and self.is_last
                else:
                    condition = self.is_first

                color_box = ColorBox(
                    bg_color=[r_bright, g_bright, b_bright, 1],
                    size=(self.cell_size, self.cell_size),
                    opacity=0 if condition else 1,
                    disabled=1 if condition else 0,
                    color_box_selection_color=[1, 1, 1, 0] if self.orientation == 'lr-tb' else [0, 0, 0, 0]
                )
                self.add_widget(color_box)
                # add entry as rgb:widget => {(255, 255, 255):ColorBox}
                self.color_boxes[tuple([int(i * 255) for i in color_box.bg_color[:-1]])] = color_box


class ColorBox(BaseLabel):
    color_box_selection_color = ColorProperty([1, 1, 1, 0])

    def on_kv_post(self, base_widget):
        self.bind(size=self.draw_color_borders, pos=self.draw_color_borders, color_box_selection_color=self.draw_color_borders)

    # update sliders with bg_color value when click on ColorBox
    def on_touch_down(self, touch):
        if not self.disabled:
            if self.collide_point(*touch.pos):
                self.set_sliders_color()
        return super().on_touch_down(touch)

    # update sliders with bg_color value when click + move over the table
    def on_touch_move(self, touch):
        if not self.disabled:
            if self.collide_point(*touch.pos):
                self.set_sliders_color()
        return super().on_touch_move(touch)

    # keep looking for set_slider_vals_from_table method by traversing parents, then apply this ColorBox bg_color value
    def set_sliders_color(self):
        parent = self.parent
        while parent:
            if hasattr(parent, 'set_slider_vals_from_table'):
                parent.set_slider_vals_from_table(self.bg_color)
                break
            parent = parent.parent

    def draw_color_borders(self, *args):
        if self.canvas is None:
            return
        self.canvas.after.clear()
        with self.canvas.after:
            Color(*self.color_box_selection_color)
            Line(
                width=dp(.75),
                rectangle=(self.x, self.y, self.width - dp(1), self.height - dp(1))
            )
