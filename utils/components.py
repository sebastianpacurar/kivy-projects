from kivy.clock import Clock
from kivy.core.window import Window
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
    project_name = StringProperty('')


class SimpleDropdown(Spinner):
    options = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(options=self.update_width)

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
    label_txt = StringProperty('')
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


class AutoSuggestionInputBox(BoxLayout):
    selected_option = StringProperty("")  # Notify changes when option is selected
    options = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_focused = False
        self.filtered_options = []
        self.highlighted_index = -1  # used to highlight selected option through Up and Down arrows
        self.is_key_down_bound = False  # prevent multiple bindings at the same time, in case of multiple suggestion boxes

    def filter_options(self, text):
        """ Filter the options based on the input text \n
            Method bound to the on_text event of input_field \n
            Filter options based on input_field text value. if empty display all options \n
            Set filtered_options then call update_options() for option re-rendering
        """
        text = text.lower()
        if text:
            self.filtered_options = [opt for opt in self.options if opt.lower().startswith(text)]
        else:
            self.filtered_options = self.options
        self.update_options()

    def update_options(self):
        """ Re-render the displayed options \n
            Clear dropdown options, then add them based on the filtered text value \n
            Bind the select_option(option_value) to the on_release button where option_value is the button text
        """
        self.ids.options_layout.clear_widgets()

        if self.ids.dropdown.opacity == 1:  # only add buttons if dropdown is visible
            for index, option in enumerate(self.filtered_options):
                btn = Button(
                    text=option,
                    size_hint_y=None,
                    height=40,
                    on_release=lambda b=option: self.select_option(b.text),
                    background_normal='',
                    background_color=(.2, .2, .2, 1)
                )
                if index == self.highlighted_index:
                    btn.background_color = (0.3, 0.6, 0.3, 1)
                self.ids.options_layout.add_widget(btn)

    def show_options(self, focus):
        """ Show or hide the dropdown options based on focus state \n
            Method bound to the on_focus event of input_field \n
            Bind/Unbind on_key_down() based on focus \n
            Clear all option widgets when losing focus
        """
        self.is_focused = focus
        self.ids.dropdown.opacity = int(focus)  # control visibility based on focus
        if focus and not self.ids.input_field.text:
            self.filtered_options = self.options
            self.update_options()
        if focus and not self.is_key_down_bound:
            Window.bind(on_key_down=self.on_key_down)
            self.is_key_down_bound = True
        elif not focus:
            Window.unbind(on_key_down=self.on_key_down)
            self.is_key_down_bound = False
            # destroy option widgets AFTER select_option() gets executed
            Clock.schedule_once(self.clear_widgets_after_delay, 0.05)

    def clear_widgets_after_delay(self, dt):
        """ Clear the widgets after a delay \n
            Used to remove dropdown options widgets, after select_option() gets executed, if it's the case \n
            This method is used to trigger clear_widgets() after option is selected through mouse click \n
            It also defaults input_text to selected_option, in case the user changes the text, without applying option, and defocuses from input
        """
        self.ids.input_field.text = self.selected_option
        self.ids.options_layout.clear_widgets()

    def select_option(self, option_value):
        """ Select the highlighted option, reset highlight index and hide the dropdown \n
            Update selected_option listener
        """
        self.ids.input_field.text = option_value
        self.selected_option = option_value
        self.ids.dropdown.opacity = 0
        self.highlighted_index = -1

    def on_key_down(self, window, keycode, scancode, modifiers, is_keyboard):
        """ Handle keyboard events for up, down, enter, escape, and backspace \n
            Up Arrow - select next upward dropdown option \n
            Down Arrow - select next downward dropdown option \n
            Enter - apply currently selected option value \n
            Escape - defocus input box, remove dropdown options
        """
        if self.is_focused and self.ids.dropdown.opacity == 1:  # applicable only when options are displayed
            if keycode == 273:  # 'Up' arrow key
                self.highlighted_index = (self.highlighted_index - 1) % len(self.filtered_options)
                self.update_options()
                return True
            elif keycode == 274:  # 'Down' arrow key
                self.highlighted_index = (self.highlighted_index + 1) % len(self.filtered_options)
                self.update_options()
                return True
            elif keycode == 13:  # 'Enter' key
                if self.highlighted_index >= 0:
                    self.select_option(self.filtered_options[self.highlighted_index])
                return True
            elif keycode == 27:  # 'Escape' key
                self.highlighted_index = -1
                self.update_options()
                self.ids.dropdown.opacity = 0
                self.ids.input_field.focus = False
                return True
        return False

class RV(RecycleView):
    pass
