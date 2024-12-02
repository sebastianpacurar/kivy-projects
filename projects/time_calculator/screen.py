from kivy.properties import DictProperty
from kivy.uix.screenmanager import Screen


class TimeCalculatorScreen(Screen):
    timer = DictProperty({'hours': 0, 'minutes': 0, 'seconds': 0})
    list_data = DictProperty()

    def _get_input_values(self):
        """
        Get user input values from TextInput elements.
        Return a tuple of the form (minutes, seconds)
        """
        minutes = int(self.ids.minutes_input_field.ids.text_input.text)
        seconds = int(self.ids.seconds_input_field.ids.text_input.text)
        return minutes, seconds

    def add_minutes_and_seconds(self):
        """
        Adds the minutes and seconds entered by the user to the current timer.
        The timer will handle overflow of seconds to minutes and minutes to hours.
        Update timer dictionary.
        """
        minutes, seconds = self._get_input_values()

        if minutes > 0 or seconds > 0:
            self.timer['seconds'] += seconds
            self.timer['minutes'] += self.timer['seconds'] // 60
            self.timer['seconds'] %= 60

            self.timer['minutes'] += minutes
            self.timer['hours'] += self.timer['minutes'] // 60
            self.timer['minutes'] %= 60

    def subtract_minutes_and_seconds(self):
        """
        Subtracts the minutes and seconds entered by the user from the current timer.
        If the subtracted time is greater than the current time, the timer is reset to 0.
        """
        if any([i for i in self.timer.values()]):
            minutes, seconds = self._get_input_values()
            total_seconds = self.timer['hours'] * 3600 + self.timer['minutes'] * 60 + self.timer['seconds']
            subtracted_seconds = minutes * 60 + seconds

            if subtracted_seconds > total_seconds:
                self.timer['hours'] = 0
                self.timer['minutes'] = 0
                self.timer['seconds'] = 0
            else:
                total_seconds -= subtracted_seconds
                self.timer['hours'] = total_seconds // 3600
                self.timer['minutes'] = (total_seconds % 3600) // 60
                self.timer['seconds'] = total_seconds % 60

    def reset_inputs(self):
        """
        Resets the input fields for minutes and seconds to "0", and focuses the minutes input field.
        """
        self.ids.minutes_input_field.ids.text_input.text = '0'
        self.ids.seconds_input_field.ids.text_input.text = '0'
        self.ids.minutes_input_field.ids.text_input.focus = True
