from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty

from custom_components.BaseComponents.base_components import BaseButtonBehavior


class SimpleButton(BaseButtonBehavior):
    label_text = StringProperty(' ')
    min_width = NumericProperty(0)
    font_size = NumericProperty(sp(16))

    def on_min_width(self, instance, value):
        self.width = value
        text_label = self.ids.text_label
        text_label.text_size = (value - dp(10), None)
