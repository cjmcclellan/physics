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
            '2.0 A·Ω'

        Value instances can also work with numpy ndarray.  Make sure the dtype of the np.ndarray is **object**::
            resistance = Value(value=1.0, unit=ureg.ohm)
            array = np.array([resistance, resistance, resistance], dtype=object)
            current = Value(value=2.0, unit=ureg.amp)
            voltage = current * resistance
            print(voltage)
            ndarray([2.0 A·Ω, 2.0 A·Ω, 2.0 A·Ω])
    """
    def __init__(self, field):

        assert field in available_fields.keys(), 'Your chosen field {} is not in list of available fields. See Docs.'.format(field)

        self.field = field

        # for comparing if two param types are the same

    def __eq__(self, other):

        # Check they are both paramtype
        if isinstance(other, Field):
            # check they are the same
            return self.field == other.field

        # if other is not paramtype, then they are not the same
        else:
            return False

    # hash for using a as dict key
    def __hash__(self):
        return hash((self.field,))

    # string operator
    def __str__(self):
        return str(self.field + ' ' + available_fields[self.field])
