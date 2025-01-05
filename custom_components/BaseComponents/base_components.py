from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.label import Label

class BaseButton(Button):
    min_width = NumericProperty(dp(100))

    def on_kv_post(self, base_widget):
        if self.parent and self.parent.width > self.min_width:
            self.min_width = self.parent.width - dp(20)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                # if left click, proceed with the button press logic
                return super(Button, self).on_touch_down(touch)
            if touch.button == 'right':
                # do nothing if right click
                return False


class BaseLabel(Label):
    bg_color = ListProperty([1, 1, 1, 0])  # default to transparent


class TextLabel(BaseLabel):
    pass
