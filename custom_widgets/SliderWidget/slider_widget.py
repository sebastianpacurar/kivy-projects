from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, ColorProperty, ObjectProperty, ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout


class SliderWidget(BoxLayout):
    """ target_prop_attribute = the kivy property which will hold the value \n
        slider_value_func = the callback for when the value changes \n
        is_int = use int value representation. if False it uses float
    """
    label_text = StringProperty('')
    target_prop_attribute = StringProperty('')
    slider_height = NumericProperty(dp(30))
    track_color = ColorProperty([1, 1, 1, 1])
    min_max = ListProperty([0, 100])
    slider_value_func = ObjectProperty(None)
    default_value = NumericProperty(0)
    is_int = BooleanProperty(True)

    def on_slider_value_func(self, instance, value):
        self.ids.slider_w.bind(value=self.slider_value_func)
