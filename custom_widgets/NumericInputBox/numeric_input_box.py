from kivy.properties import BooleanProperty, StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class NumericInputBox(BoxLayout):
    is_readonly = BooleanProperty(False)
    allow_float = BooleanProperty(False)
    is_validate_digits = BooleanProperty(True)
    label_text = StringProperty('')
    container_width = NumericProperty(0)
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
