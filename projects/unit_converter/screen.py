from kivy.uix.screenmanager import Screen


class UnitConverterScreen(Screen):
    conversion_factors = {
        # Metric
        'nanometer [nm]': 1e9,  # 1 nm = 1e-9 meters
        'micrometer [µm]': 1e6,  # 1 µm = 1e-6 meters
        'millimeter [mm]': 1000.0,  # 1 mm = 0.001 meters
        'centimeter [cm]': 100.0,  # 1 cm = 0.01 meters
        'decimeter [dm]': 10.0,  # 1 dm = 0.1 meters
        'meter [m]': 1.0,  # Base unit
        'decameter [dam]': 0.1,  # 1 dam = 10 meters
        'hectometer [hm]': 0.01,  # 1 hm = 100 meters
        'kilometer [km]': 0.001,  # 1 km = 1000 meters
        'megameter [Mm]': 1e-6,  # 1 Mm = 1,000,000 meters

        # Yard
        'thou [th]': 39370.1,  # 1 thou (mil) = 0.0000254 meters
        'inch [in]': 39.3701,  # 1 inch = 0.0254 meters
        'hand': 9.84252,  # 1 hand = 0.1016 meters
        'foot [ft]': 3.28084,  # 1 foot = 0.3048 meters
        'yard [yd]': 1.09361,  # 1 yard = 0.9144 meters
        'furlong': 0.00497096,  # 1 furlong = 201.168 meters
        'mile [mi]': 0.000621371,  # 1 mile = 1609.34 meters
        'league [lea]': 0.000207123,  # 1 league = 4828.03 meters

        # Nautical
        'cable': 0.000539957 * 0.1,  # 1 cable = 185.2 meters
        'nautical mile [nmi]': 0.000539957,  # 1 nautical mile = 1852 meters

        # Outer Space
        'astronomical unit [au]': 6.68459e-12,  # 1 AU = 1.496e11 meters
        'parsec [pc]': 3.24078e-17,  # 1 parsec = 3.086e16 meters
        'light-year [ly]': 1.057e-16,  # 1 light-year = 9.461e15 meters
        'kiloparsec [kpc]': 3.24078e-20,  # 1 kiloparsec = 3.086e19 meters
        'megaparsec [Mpc]': 3.24078e-23  # 1 megaparsec = 3.086e22 meters
    }

    def on_enter(self, *args):
        """ Screen Setup \n
            Set numeric inputs to 1, from_conversion to 'meter [m]' and to_conversion to 'yard [yd]'
        """
        self.set_default_option()
        self.ids.from_selection.bind(selected_option=self.os_suggestion_box_update)
        self.ids.target_selection.bind(selected_option=self.os_suggestion_box_update)

    def os_suggestion_box_update(self, *args):
        """ Listens for changes of the selected_option StringProperty() \n
            If any change occurred, then update target input \n
            Used to update input when changing comparison_factors from the AutoSuggestionBox
        """
        self.update_target_input()

    def set_options(self):
        return list(self.conversion_factors.keys())

    def set_default_option(self):
        """ Set default options for conversion: 'meter [m]' to 'yard [yd]' \n
            Toggle focus on inputs to hide the displayed default dropdown option \n
            Set default compared value to 1
        """
        self.ids.from_selection.ids.input_field.text = 'meter [m]'
        self.ids.from_selection.ids.input_field.focus = True
        self.ids.from_selection.ids.input_field.focus = False
        self.ids.target_selection.ids.input_field.text = 'yard [yd]'
        self.ids.target_selection.ids.input_field.focus = True
        self.ids.target_selection.ids.input_field.focus = False
        self.ids.from_input_field.ids.text_input.text = '1'

    def update_target_input(self):
        """ Perform conversion from one unit to another, if from_input is greater than 0 """
        if len(self.ids.from_input_field.ids.text_input.text) > 0:
            from_value = float(self.ids.from_input_field.ids.text_input.text)
            from_selection = self.ids.from_selection.ids.input_field.text
            target_selection = self.ids.target_selection.ids.input_field.text
            converted_val = self.convert_length(from_value, from_selection, target_selection)
            self.ids.target_input_field.ids.text_input.text = converted_val

    def convert_length(self, value, from_unit, to_unit):
        """ Converts length between units relative to meters """

        # convert from the given unit to meters
        value_in_meters = value / self.conversion_factors[from_unit]

        # convert from meters to the target unit
        converted_value = value_in_meters * self.conversion_factors[to_unit]
        return str(converted_value)
