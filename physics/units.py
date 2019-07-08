import pint

ureg = pint.UnitRegistry()

unit_options = {
    'unitless': ureg.dimensionless,
    'ohm': ureg.ohm,
    'coulomb': ureg.coulomb,
    'second': ureg.second,
    'faraday / meter': ureg.faraday / ureg.meter,
    'volt': ureg.volt,
    'meter': ureg.meter,
    'meter ** 2': ureg.meter * ureg.meter,
    'meter * ohm': ureg.ohm * ureg.meter,
    # 'micrometer': ureg.micrometer,
    # 'micrometer * kiloohm': ureg.micrometer * ureg.kiloohm,
    'meter ** 2 * ohm': ureg.ohm * ureg.meter * ureg.meter,
}

unit_options_str = {unit: '{:~P}'.format(unit_pint.encode()) for unit, unit_pint in unit_options.items()}

prefix_options = {
    ('nano', 'n'): 1e-9,
    ('micro', '\u03BC'.encode()): 1e-6,
    ('milli', 'm'): 1e-3,
    ('centi', 'c'): 1e-2,
    ('', ''): 1,
    ('kilo', 'K'): 1e3,
    ('mega', 'M'): 1e6,
    ('giga', 'G'): 1e9,
    ('tera', 'T'): 1e12,
}

# unit_options = {
#     'Ohm': '\u03A9',
#     'meter': 'm',
#     'Ohm-meter': '\u03A9*m',
#     'meter-squared': 'm*m'
# }

derived_units = {
    'mobility': ''
}

# the available operations of units
operations = {'divide': '/', 'multiply': '*'}

complete_units = [(unit_pint * prefix).to_compact().units for prefix in prefix_options.values() for unit_pint in unit_options.values()]
complete_units_dict = {'{:~P}'.format((unit_pint * prefix).to_compact().units): (unit_pint * prefix).to_compact().units for
                       prefix in prefix_options.values() for unit_pint in unit_options.values()}

complete_units_str = {'{}'.format(unit_pint): '{:~P}'.format(unit_pint) for unit_pint in complete_units}

all_units = {unit: [(unit_pint * prefix).to_compact().units for prefix in prefix_options.values()] for unit, unit_pint in unit_options.items()}

# list all the available units
# all_units = [prefix[1] + unit for prefix in prefix_options.keys() for unit in unit_options.values()]

# useful for dash dropdown options
all_unit_options = {unit: [{'label': '{:~P}'.format(unit_pint), 'value': '{:~P}'.format(unit_pint)} for unit_pint in all_units[unit]]
                    for unit in all_units.keys()}


def str_to_pint(string):
    """Converts a string to a Pint Unit

        Args:
            :param string: the unit string to be converted
            :type str: python string class

        Returns:
            :return pint.unit: Returns a unit for this string

        Errors:
            Raises an error if the unit string is not allowed

        For Example:

        >>> str_to_pint('Ω')
        pint.unit(ohm)
    """
    try:
        return complete_units_dict[string]
    except Exception:
        raise EnvironmentError('The string {} is not in the allowed units'.format(string))


def pint_to_str(pint_unit):

    """Converts a Pint.Unit to a string

        Args:
            :param pint_unit: the unit to be converted to string
            :type pint.unit: Pint Unit object instance

        Returns:
            :return string: Returns a string of this unit

        For Example:

        >>> pint_to_str(ureg.ohm)
        'Ω'
    """

    return '{:~P}'.format(pint_unit)


# # split units into basic units (i.e. removing operations)
# def split_units(unit):
#     assert isinstance(unit, str), 'The unit must be in str form.'
#     assert unit.count(operations['divide']) < 2, 'You can only have one divide in the unit.'
#     # oder of operations says divide goes first
#     units_div = unit.split(operations['divide'])
#     # now loop through each unit and break apart
#     units = []
#     for u in units_div:
#         units.append(u.split(operations['multiply']))
#     return units
#
#
# # function to convert prefixes to orders of magnitude
# def prefix_to_magnitude(unit):
#     units = split_units(unit)
#     prefix_mag = 1
#     # will be a 2D array with the first layer being separated by divide and second by multiplies
#     for u_mul in units[0]:
#         pass



