from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.spinner import Spinner


class AppBtn(Button):
    pass


class AppLabel(Label):
    bg_color = ListProperty([1, 1, 1, 0])  # default to transparent


class TopBar(BoxLayout):
    project_name = StringProperty()


class AppDropdown(Spinner):
    options = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(options=self.update_width)

    def on_spinner_select(self, spinner, text):
        print(f"Selected: {text}")

    def update_width(self, *args):
        """Update width based on the longest option in the dropdown."""
        longest_option = max(self.options, key=len)  # Find the longest option by character length
        # Calculate the width of the longest option
        self.width = max(self.texture_size[0], len(longest_option) * dp(10))

    def on_kv_post(self, base_widget):
        pass


class LabeledNumericInput(BoxLayout):
    is_readonly = BooleanProperty(False)
    allow_float = BooleanProperty(False)
    is_validate_digits = BooleanProperty(True)
    label_txt = StringProperty()
    container_width = NumericProperty()
    update_text_field_func = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        """Initial value set to 0 and set up event handlers"""
        self.ids.text_input.text = "0"
        text_input = self.ids.text_input

        # bind validate_digits if is_validate_digits is set to True
        if self.is_validate_digits:
            text_input.bind(text=self.validate_digits)

        # bind custom function (update_text_field_func) when on_text triggers
        if self.update_text_field_func:
            text_input.bind(text=self.update_text_field_func)



    def validate_digits(self, instance, value):
        """ Forces TextInput to use only integers or floats, based on the 'allow_float' BooleanProperty """
        text_field = self.ids.text_input

        if self.allow_float:
            # allow digits and a single '.'
            filtered_text = ''.join([i for i in text_field.text if i.isdigit() or i == '.'])

            # do not allow period as the first char
            if filtered_text.startswith('.'):
                filtered_text = ''

            # ensure there's only one '.'
            if filtered_text.count('.') > 1:
                parts = filtered_text.split('.')
                filtered_text = parts[0] + '.' + ''.join(parts[1:])

            # allow leading zero but validate correctly -> "0." allowed
            if len(filtered_text) > 1 and filtered_text.startswith('0') and filtered_text[1] != '.':
                filtered_text = filtered_text[1:]

            text_field.text = filtered_text
        else:
            # allow only digits
            text_field.text = ''.join([i for i in text_field.text if i.isdigit()])

            # prevent leading zero unless it's the only character
            if len(text_field.text) > 1 and text_field.text.startswith('0'):
                text_field.text = text_field.text[1:]


class RV(RecycleView):
    pass
