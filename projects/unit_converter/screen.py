from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from projects.unit_converter.conversion_units import *


class UnitConverterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = self.ids.screen_manager
        self.curr_screen_index = 0

    def change_unit_screen(self, button, unit_screen_name):
        if button.state == 'down':
            self.sm.transition.direction = 'left' if button.option_index > self.curr_screen_index else 'right'
            self.curr_screen_index = button.option_index
            self.sm.current = unit_screen_name


class BaseUnitScreen(Screen):
    def __init__(self, screen, unit_type, initial_conversion, **kw):
        super().__init__(**kw)
        self.screen = screen
        self.unit_type = unit_type
        self.initial_conversion = initial_conversion

    def on_kv_post(self, base_widget):
        """ Screen Setup \n
            Set numeric inputs to 1, from_conversion to 'meter [m]' and to_conversion to 'yard [yd]' \n
            Bind os_suggestion_box_update to the state of selected_option property, for both boxes
        """

        self.set_default_option()
        self.screen.ids.converter.ids.from_selection.bind(selected_option=self.os_suggestion_box_update)
        self.screen.ids.converter.ids.target_selection.bind(selected_option=self.os_suggestion_box_update)

    def os_suggestion_box_update(self, *args):
        """ Listens for changes of the selected_option StringProperty() \n
            If any change occurred, then update target input \n
            Used to update input when changing comparison_factors from the AutoSuggestionBox
        """
        self.update_target_input()

    def set_default_option(self):
        """ Set default options for conversion: ex: 'meter [m]' to 'yard [yd]' \n
            Toggle focus on inputs to hide the displayed default dropdown option \n
            Set default compared value to 1
        """
        self.screen.ids.converter.ids.from_selection.ids.input_field.text = self.initial_conversion[0]
        self.screen.ids.converter.ids.from_selection.ids.input_field.focus = True
        self.screen.ids.converter.ids.from_selection.ids.input_field.focus = False
        self.screen.ids.converter.ids.target_selection.ids.input_field.text = self.initial_conversion[1]
        self.screen.ids.converter.ids.target_selection.ids.input_field.focus = True
        self.screen.ids.converter.ids.target_selection.ids.input_field.focus = False
        self.screen.ids.converter.ids.from_input_field.ids.text_input.text = '1'

    def update_target_input(self):
        """ Perform conversion from one unit to another, if from_input is greater than 0 """
        if len(self.screen.ids.converter.ids.from_input_field.ids.text_input.text) > 0:
            from_value = float(self.screen.ids.converter.ids.from_input_field.ids.text_input.text)
            from_selection = self.screen.ids.converter.ids.from_selection.ids.input_field.text
            target_selection = self.screen.ids.converter.ids.target_selection.ids.input_field.text
            converted_val = convert(from_value, from_selection, target_selection, self.unit_type)
            self.screen.ids.converter.ids.target_input_field.ids.text_input.text = converted_val


class LengthScreen(BaseUnitScreen):
    def __init__(self, **kw):
        super().__init__(screen=self, unit_type='length', initial_conversion=['meter [m]', 'yard [yd]'], **kw)

    def set_options(self):
        return list(length_conversion_factors.keys())


class AreaScreen(BaseUnitScreen):
    def __init__(self, **kw):
        super().__init__(screen=self, unit_type='area',
                         initial_conversion=['square meter [m²]', 'square centimeter [cm²]'], **kw)

    def set_options(self):
        return list(area_conversion_factors.keys())


class VolumeScreen(BaseUnitScreen):
    def __init__(self, **kw):
        super().__init__(screen=self, unit_type='volume', initial_conversion=['liter [L]', 'cubic meter [m³]'], **kw)

    def set_options(self):
        return list(volume_conversion_factors.keys())


class EnergyScreen(BaseUnitScreen):
    def __init__(self, **kw):
        super().__init__(screen=self, unit_type='energy', initial_conversion=['joule [J]', 'calorie [cal]'], **kw)

    def set_options(self):
        return list(energy_conversion_factors.keys())


class ForceScreen(BaseUnitScreen):
    def __init__(self, **kw):
        super().__init__(screen=self, unit_type='force', initial_conversion=['newton [N]', 'gram-force [gf]'], **kw)

    def set_options(self):
        return list(force_conversion_factors.keys())


class SpeedScreen(BaseUnitScreen):
    def __init__(self, **kw):
        super().__init__(screen=self, unit_type='speed', initial_conversion=['meter per second [m/s]', 'inch per second [in/s]'], **kw)

    def set_options(self):
        return list(speed_conversion_factors.keys())


class Converter(GridLayout):
    drop_options = ListProperty([])
    source_selected_option = StringProperty()
    target_selected_option = StringProperty()
    update_text_field_func = ObjectProperty(None)
