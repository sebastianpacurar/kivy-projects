from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, ColorProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class SliderWidget(BoxLayout):
    """ target_prop_attribute = the kivy property which will hold the value \n
        slider_value_func = the callback for when the value changes \n
    """
    label_text = StringProperty('')
    target_prop_attribute = StringProperty('')
    slider_height = NumericProperty(dp(30))
    current_value = NumericProperty(0)
    track_color = ColorProperty([1, 1, 1, 1])
    min_val = NumericProperty(0)
    max_val = NumericProperty(100)
    slider_value_func = ObjectProperty(None)

    def on_slider_value_func(self, instance, value):
        self.ids.slider_w.bind(value=self.slider_value_func)
