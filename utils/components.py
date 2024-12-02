from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView


class AppBtn(Button):
    pass


class AppLabel(Label):
    bg_color = ListProperty([1, 1, 1, 0])  # default to transparent


class TopBar(BoxLayout):
    project_name = StringProperty()


class LabeledNumericInput(BoxLayout):
    label_txt = StringProperty()
    container_width = NumericProperty()

    def on_kv_post(self, base_widget):
        """Initial value set to 0"""
        self.ids.text_input.text = "0"

    def validate_digits(self, instance, value):
        """ Forces TextInput to use only integers """
        text_field = self.ids.text_input
        text_field.text = ''.join([i for i in text_field.text if i.isdigit()])
        if len(text_field.text) > 1 and text_field.text.startswith('0'):
            text_field.text = text_field.text[1:]


class RV(RecycleView):
    pass
