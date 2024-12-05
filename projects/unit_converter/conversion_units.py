length_conversion_factors = {
    # Metric
    'nanometer [nm]': 1e9,  # 1 nm = 1e-9 meters
    'micrometer [µm]': 1e6,  # 1 µm = 1e-6 meters
    'millimeter [mm]': 1000.0,  # 1 mm = 0.001 meters
    'centimeter [cm]': 100.0,  # 1 cm = 0.01 meters
    'decimeter [dm]': 10.0,  # 1 dm = 0.1 meters
    'meter [m]': 1.0,  # base unit
    'decameter [dam]': 0.1,  # 1 dam = 10 meters
    'hectometer [hm]': 0.01,  # 1 hm = 100 meters
    'kilometer [km]': 0.001,  # 1 km = 1000 meters
    'megameter [Mm]': 1e-6,  # 1 Mm = 1,000,000 meters

    # Yard
    'thou [th]': 2.54e-5,  # 1 thou (mil) = 0.0000254 meters (corrected)
    'inch [in]': 39.3701,  # 1 inch = 0.0254 meters
    'hand [hd]': 9.84252,  # 1 hand = 0.1016 meters
    'foot [ft]': 3.28084,  # 1 foot = 0.3048 meters
    'yard [yd]': 1.09361,  # 1 yard = 0.9144 meters
    'furlong': 0.00497096,  # 1 furlong = 201.168 meters
    'mile [mi]': 0.000621371,  # 1 mile = 1609.34 meters
    'league [lea]': 0.000207123,  # 1 league = 4828.03 meters

    # Nautical
    'cable [cb]': 185.2,  # 1 cable = 185.2 meters (corrected)
    'nautical mile [nmi]': 0.000539957,  # 1 nautical mile = 1852 meters

    # Outer Space
    'astronomical unit [au]': 6.68459e-12,  # 1 AU = 1.496e11 meters
    'parsec [pc]': 3.24078e-17,  # 1 parsec = 3.086e16 meters
    'light-year [ly]': 1.057e-16,  # 1 light-year = 9.461e15 meters
    'kiloparsec [kpc]': 3.24078e-20,  # 1 kiloparsec = 3.086e19 meters
    'megaparsec [Mpc]': 3.24078e-23  # 1 megaparsec = 3.086e22 meters
}

area_conversion_factors = {
    'square millimeter [mm²]': 1e6,  # 1 mm² = 1e-6 m²
    'square centimeter [cm²]': 1e4,  # 1 cm² = 1e-4 m²
    'square meter [m²]': 1.0,  # base unit
    'square kilometer [km²]': 1e-6,  # 1 km² = 1e-6 m²
}

volume_conversion_factors = {
    'cubic millimeter [mm³]': 1e9,  # 1 mm³ = 1e-9 m³
    'cubic centimeter [cm³]': 1e6,  # 1 cm³ = 1e-6 m³
    'liter [L]': 1000.0,  # 1 L = 1e3 m³
    'cubic meter [m³]': 1.0,  # base unit
    'cubic kilometer [km³]': 1e-9,  # 1 km³ = 1e-9 m³
}

energy_conversion_factors = {
    'joule [J]': 1.0,  # base unit
    'kilojoule [kJ]': 0.001,  # 1 kJ = 1000 J
    'megajoule [MJ]': 1e-6,  # 1 MJ = 1,000,000 J
    'gigajoule [GJ]': 1e-9,  # 1 GJ = 1e9 J
    'calorie [cal]': 0.239006,  # 1 cal = 4.184 J
    'kilocalorie [kcal]': 0.000239006,  # 1 kcal = 4184 J
    'watt-hour [Wh]': 0.000277778,  # 1 Wh = 3600 J
    'kilowatt-hour [kWh]': 2.77778e-7,  # 1 kWh = 3.6e6 J
    'electronvolt [eV]': 6.242e18,  # 1 eV = 1.60218e-19 J
    'british thermal unit [BTU]': 0.000947817,  # 1 BTU = 1055.06 J
    'foot-pound [ft-lb]': 0.737562,  # 1 ft-lb = 1.35582 J
    'erg': 1e7,  # 1 erg = 1e-7 J
    'therm [thm]': 9.48043e-9,  # 1 therm = 1.05506e8 J
}

force_conversion_factors = {
    'newton [N]': 1.0,  # base unit
    'kilonewton [kN]': 0.001,  # 1 kN = 1000 N
    'dyne [dyn]': 1e5,  # 1 dyn = 1e-5 N
    'kilogram-force [kgf]': 0.101972,  # 1 kgf = 9.80665 N
    'pound-force [lbf]': 0.224809,  # 1 lbf = 4.44822 N
    'ton-force (short) [tonf]': 0.000112404,  # 1 tonf = 2000 lbf
    'ton-force (metric) [tf]': 0.000101972,  # 1 tf = 1000 kgf
    'ounce-force [ozf]': 3.59694,  # 1 ozf = 0.2780139 N
    'gram-force [gf]': 101.972,  # 1 gf = 0.00980665 N
}

speed_conversion_factors = {
    'meter per second [m/s]': 1.0,  # base unit
    'kilometer per hour [km/h]': 3.6,  # 1 m/s = 3.6 km/h
    'kilometer per second [km/s]': 0.001,  # 1 m/s = 0.001 km/s
    'mile per hour [mph]': 2.23694,  # 1 m/s = 2.23694 mph
    'foot per second [ft/s]': 3.28084,  # 1 m/s = 3.28084 ft/s
    'mile per second [mi/s]': 0.000621371,  # 1 m/s = 0.000621371 mi/s
    'inch per second [in/s]': 39.3701,  # 1 m/s = 39.3701 in/s
    'knot [kn]': 1.94384,  # 1 m/s = 1.94384 knots
    'mach (at sea level)': 0.00293858,  # 1 m/s = 0.00293858 Mach
    'speed of light [c]': 3.33564e-9,  # 1 m/s = 1/299792458 c
}


def convert(value, from_unit, to_unit, unit_type):
    """Generalized method to convert length, area, or volume"""

    # Select the appropriate conversion factors based on the unit type
    if unit_type == 'length':
        conversion_factors = length_conversion_factors
    elif unit_type == 'area':
        conversion_factors = area_conversion_factors
    elif unit_type == 'volume':
        conversion_factors = volume_conversion_factors
    elif unit_type == 'energy':
        conversion_factors = energy_conversion_factors
    elif unit_type == 'force':
        conversion_factors = force_conversion_factors
    elif unit_type == 'speed':
        conversion_factors = speed_conversion_factors
    else:
        raise ValueError(f"Invalid unit type: {unit_type}")

    # Convert from the given unit to the base unit
    value_in_base_unit = value / conversion_factors[from_unit]

    # Convert from the base unit to the target unit
    converted_value = value_in_base_unit * conversion_factors[to_unit]

    return str(converted_value)
