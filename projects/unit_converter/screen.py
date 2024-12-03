from kivy.uix.screenmanager import Screen


class UnitConverterScreen(Screen):

    def update_to_input(self):
        if len(self.ids.from_input_field.ids.text_input.text) > 0:
            from_value = float(self.ids.from_input_field.ids.text_input.text)
            converted_val = convert_length(from_value, self.ids.from_dropdown.text, self.ids.to_dropdown.text)
            self.ids.to_input_field.ids.text_input.text = converted_val


def convert_length(value, from_unit, to_unit):
    """ Converts length between units relative to meters """
    conversion_factors = {
        'kilometer [km]': 0.001,  # 1 km = 1000 meters
        'meter [m]': 1.0,
        'decimeter [dm]': 10.0,  # 1 dm = 0.1 meters
        'centimeter [cm]': 100.0,  # 1 cm = 0.01 meters
        'millimeter [mm]': 1000.0,  # 1 mm = 0.001 meters
    }

    # convert from the given unit to meters
    value_in_meters = value / conversion_factors[from_unit]

    # convert from meters to the target unit
    converted_value = value_in_meters * conversion_factors[to_unit]
    return str(converted_value)
