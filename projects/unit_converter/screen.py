from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from projects.unit_converter.conversion_units import *


class UnitConverterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = self.ids.screen_manager
        self.curr_screen_index = 0

    def change_unit_screen(self, instance, value):
        if not hasattr(self, 'curr_screen_index'):
            return
        if value == 'down':
            self.sm.transition.direction = 'left' if instance.option_index > self.curr_screen_index else 'right'
            self.curr_screen_index = instance.option_index
            self.sm.current = f'{instance.btn_text}Screen'


class BaseUnitScreen(Screen):
    initial_conversion = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        """ Screen Setup \n
            Set numeric inputs to 1, from_conversion to 'meter [m]' and to_conversion to 'yard [yd]' \n
            Bind os_suggestion_box_update to the state of selected_option property, for both boxes
        """

        self.set_default_option()
        self.ids.converter.ids.from_selection.bind(selected_option=self.os_suggestion_box_update)
        self.ids.converter.ids.target_selection.bind(selected_option=self.os_suggestion_box_update)

    def os_suggestion_box_update(self, *args):
        """ Listens for changes of the selected_option StringProperty() \n
            If any change occurred, then update target input \n
            Used to update input when changing comparison_factors from the AutoSuggestionBox
        """
        self.update_target_input()

    def set_options(self):
        return conversion_factors[self.name.split('Screen')[0].lower()].keys()

    def set_default_option(self):
        """ Set default options for conversion: ex: 'meter [m]' to 'yard [yd]' \n
            Toggle focus on inputs to hide the displayed default dropdown option \n
            Set default compared value to 1
        """
        self.ids.converter.ids.from_selection.ids.input_field.text = self.initial_conversion[0]
        self.ids.converter.ids.from_selection.ids.input_field.focus = True
        self.ids.converter.ids.from_selection.ids.input_field.focus = False
        self.ids.converter.ids.target_selection.ids.input_field.text = self.initial_conversion[1]
        self.ids.converter.ids.target_selection.ids.input_field.focus = True
        self.ids.converter.ids.target_selection.ids.input_field.focus = False
        self.ids.converter.ids.from_input_field.ids.text_input.text = '1'

    def update_target_input(self):
        """ Perform conversion from one unit to another, if from_input is greater than 0 """
        if len(self.ids.converter.ids.from_input_field.ids.text_input.text) > 0:
            from_value = float(self.ids.converter.ids.from_input_field.ids.text_input.text)
            from_selection = self.ids.converter.ids.from_selection.ids.input_field.text
            target_selection = self.ids.converter.ids.target_selection.ids.input_field.text
            converted_val = convert(from_value, from_selection, target_selection, self.name.split('Screen')[0].lower())
            self.ids.converter.ids.target_input_field.ids.text_input.text = converted_val


class LengthScreen(BaseUnitScreen):
    pass


class AreaScreen(BaseUnitScreen):
    pass


class VolumeScreen(BaseUnitScreen):
    pass


class EnergyScreen(BaseUnitScreen):
    pass


class ForceScreen(BaseUnitScreen):
    pass


class SpeedScreen(BaseUnitScreen):
    pass


class Converter(GridLayout):
    drop_options = ListProperty([])
    source_selected_option = StringProperty()
    target_selected_option = StringProperty()
    update_text_field_func = ObjectProperty(None)
