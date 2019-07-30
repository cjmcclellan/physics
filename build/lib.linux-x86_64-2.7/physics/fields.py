# H1 -- For the Field class
# *************************
from physics.units import complete_units, ureg, pint_to_str, str_to_pint
import pint
import numpy as np
import physics.conf as conf

if conf.tf_flag:
    import tensorflow as tf


# ---Give a list of the available fields--------------
available_fields = {'temperature': ureg.kelvin,
                    'heat_temperature': ureg.kelvin,
                    'heat flux': ureg.watt/(ureg.meter * ureg.meter),
                    'thermal conductivity': ureg.watt/(ureg.meter * ureg.kelvin),
                    'heat_conductivity': ureg.watt/(ureg.meter * ureg.kelvin),
                    'voltage': ureg.volt,
                    'current': ureg.amp,
                    None: None
                    }


class Field(object):
    """Field object used for assessing physical fields

        Args:
            field (str): The field name.  Should be in list of available fields.  See Docs.

        Basic Example::
            resistance = Value(value=1.0, unit=ureg.ohm)
            current = Value(value=2.0, unit=ureg.amp)
            voltage = current * resistance
            '2.0 A*Ohm'

        Value instances can also work with numpy ndarray.  Make sure the dtype of the np.ndarray is **object**::
            resistance = Value(value=1.0, unit=ureg.ohm)
            array = np.array([resistance, resistance, resistance], dtype=object)
            current = Value(value=2.0, unit=ureg.amp)
            voltage = current * resistance
            print(voltage)
            ndarray([2.0 A*Ohm, 2.0 A*Ohm, 2.0 A*Ohm])
    """
    def __init__(self, field, name=None, unit=None):

        assert field in available_fields.keys(), 'Your chosen field {} is not in list of available fields. See Docs.'.format(field)

        self.field = field

        # the name of this field
        self.name = name

        # if unit is none, then use the default unit
        if unit is None:
            self.unit = available_fields[self.field]
        else:
            assert isinstance(unit, pint.unit._Unit), 'Your unit for this field must be from physics.value.ureg.'
            assert unit.dimensionality ==\
                   available_fields[self.field].dimensionality, 'Your input unit does not have the right dimensions.' \
                                                                ' You gave {0} but it should be {1}.'.format(unit.dimensionality, available_fields[self.field].dimensionality)
            self.unit = unit
        # for comparing if two param types are the same

    def __eq__(self, other):

        # Check they are both paramtype
        if isinstance(other, Field):
            # check they are the same
            return self.field == other.field and self.name == other.name

        # if other is not paramtype, then they are not the same
        else:
            return False

    # hash for using a as dict key
    def __hash__(self):
        return hash((self.field, self.name))

    # string operator
    def __str__(self):
        return '{0} {1}'.format(self.name, self.field)
