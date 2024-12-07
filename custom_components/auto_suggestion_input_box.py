from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class AutoSuggestionInputBox(BoxLayout):
    selected_option = StringProperty("")  # Notify changes when option is selected
    options = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mark_started = False
        self.is_focused = False
        self.is_auto_selected = False
        self.highlighted_index = -1  # used to highlight selected option through Up and Down arrows
        self.is_key_down_bound = False  # prevent multiple bindings at the same time, in case of multiple suggestion boxes
        self.filtered_options = []
        self.preprocessed_options = []  # preprocess options for faster matching

    def on_kv_post(self, base_widget):
        self.preformat_options_for_filtering()

    def preformat_options_for_filtering(self):
        """ Store options in a tuple form for faster filtering \n
            ex: 'meter [m]' = ('meter [m]', ['meter', 'm']) \n
            ex: 'astronomical unit [au]' = ('astronomical unit [au]', ['astronomical', 'unit', 'au'])
        """
        self.preprocessed_options = [
            (opt, opt.lower().replace('[', '').replace(']', '').split())
            for opt in self.options
        ]

    def filter_options(self, text):
        """ Filter the options based on the input text \n
            Method bound to the on_text event of input_field \n
            Filter options based on input_field separated words. if empty display all options \n
            Set filtered_options then call update_options() for option re-rendering
        """
        text = text.lower()
        if text:
            # match based on split words.
            # ex: 'nautical mile [nmi]' will be displayed for 'nau*', 'mil*' and 'nmi'
            self.filtered_options = [
                original for original, words in self.preprocessed_options
                if any(word.startswith(text.lower()) for word in words)
            ]
        else:
            # display all options if no text is in input box
            self.filtered_options = self.options
        self.update_options()

    def update_options(self):
        """ Re-render the displayed options \n
            Clear dropdown options, then add them based on the filtered text value \n
            Bind the select_option(option_value) to the on_release button where option_value is the button text
        """
        self.ids.options_layout.clear_widgets()

        if self.is_focused:  # only add buttons if text input is focused
            for index, option in enumerate(self.filtered_options):
                btn = AutoSuggestionInputOption(
                    text=option,
                    on_release=lambda b=option: self.select_option(b.text),
                )
                # auto highlight the only displayed option
                if len(self.filtered_options) == 1 and not self.is_auto_selected:
                    self.highlighted_index = index
                    self.is_auto_selected = True
                # if more than 2 options displayed, and not auto highlighted, set to -1
                elif len(self.filtered_options) > 1 and self.is_auto_selected:
                    self.highlighted_index = -1
                    self.is_auto_selected = False
                # set color for highlighted button
                if index == self.highlighted_index:
                    btn.background_color = (0.3, 0.6, 0.3, 1)

                self.ids.options_layout.add_widget(btn)

    def show_options(self, focus):
        """ Show or hide the dropdown options based on focus state \n
            Method bound to the on_focus event of input_field \n
            Handle dynamic user input - delete when focus changes to True \n
            Bind/Unbind on_key_down() based on focus \n
            Clear all option widgets when losing focus
        """

        # prevent execution when screen loads for the very first time
        if not self.mark_started:
            self.mark_started = True
            return

        # set input to empty when user focuses, to prevent backspacing for every focus
        if self.is_focused is False and focus is True:
            self.ids.input_field.text = ''

        self.is_focused = focus

        self.is_focused = focus
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
        self.highlighted_index = -1

    def on_key_down(self, window, keycode, scancode, modifiers, is_keyboard):
        """ Handle keyboard events for up, down, enter, escape, and backspace \n
            Up Arrow - select next upward dropdown option \n
            Down Arrow - select next downward dropdown option \n
            Enter - defocus input box, apply currently selected option value \n
            Escape - defocus input box, remove dropdown options
        """
        if self.is_focused:
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
                    self.ids.input_field.focus = False
                return True
            elif keycode == 27:  # 'Escape' key
                self.highlighted_index = -1
                self.update_options()
                self.ids.input_field.focus = False
                return True
        return False


class AutoSuggestionInputOption(Button):
    pass