from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty

from custom_widgets.base_widgets import PropCachedWidget, BaseButtonBehavior


class IconButton(BaseButtonBehavior, PropCachedWidget):
    icon = StringProperty('')  # icon unicode
    label_text = StringProperty('')  # button label text. if empty, it's just an icon button, else labeled icon button
    bg_size_val = NumericProperty(dp(34))  # used with font_size_val to get different sized icons
    font_size_val = NumericProperty(sp(28))  # if no text label, this should be of the size of the bg_size_val
    x_padding = NumericProperty(dp(24))  # if no text, this should be 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_initialized = False

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

    def hide_widget(self, props=None):
        super().hide_widget(self.cached_props)

    def reveal_widget(self, props=None):
        super().reveal_widget()
