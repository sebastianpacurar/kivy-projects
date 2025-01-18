from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty

from custom_widgets.base_widgets import BaseButtonBehavior


class SimpleButton(BaseButtonBehavior):
    label_text = StringProperty(' ')
    wrap_width_val = NumericProperty(0)
    font_size = NumericProperty(sp(16))

    def on_wrap_width_val(self, instance, value):
        self.width = value
        text_label = self.ids.text_label
        text_label.text_size = (value - dp(10), None)
