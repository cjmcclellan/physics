# H1 -- For the Value class
# *************************
from physics.units import complete_units, ureg, pint_to_str, str_to_pint
import numpy as np

# H3 -- Value Class
# -----------------


class Value(float):

    """Value object built on the float object and using `Pint Units <https://pint.readthedocs.io/en/0.9/>`_.

        :param value: The float value
        :type value: float
        :param unit: The unit for this value
        :type unit: pint.unit

        Example:
            >>> resistance = Value(value=1.0, unit=ureg.ohm)
            >>> current = Value(value=2.0, unit=ureg.amp)
            >>> voltage = current * resistance
            '2.0 A·Ω'
    """

    def __new__(cls, value, unit=''):
        # assert unit in complete_units, 'Your unit {0} is not in the list of available units'.format(unit)
        # value, unit = cls.SI_unit(value, unit)
        return float.__new__(cls, value)

    def unit_str(self):

        """Gives the str of the unit.

            :returns str: A string of the unit

            For Example:

            >>> example = Value(value=1.0, unit=ureg.ohm)
            >>> print(example.unit_str())
            Ω
            """

        return '{:~P}'.format(self.unit)

    def __str__(self):
        return '{0} '.format(self.value) + self.unit_str()

    def __init__(self, value, unit):
        float.__init__(value)
        # make sure this is the simplest form
        # test = value * unit
        # test.to_reduced_units()
        self.unit = unit
        self.value = value

    def adjust_unit(self, desired_unit):
        tmp = self.value*self.unit
        tmp = tmp.to(desired_unit)
        return Value(tmp.magnitude, tmp.units)

    def simplify_units(self):
        tmp = self.value*self.unit
        tmp = tmp.to_reduced_units().to_compact()
        return Value(tmp.magnitude, tmp.units)

    def compact_units(self):
        tmp = self.value * self.unit
        tmp = tmp.to_compact()
        return Value(tmp.magnitude, tmp.units)

    def __round__(self, n=None):
        return Value(value=float.__round__(self, n), unit=self.unit)

    def __mul__(self, other):
        # check if this is an ndarray, if so cast the value to an array of the same shape
        if isinstance(other, np.ndarray):
            return other * np.array([self], dtype=object)

        if not isinstance(other, Value):
            return Value(value=other*self.value, unit=self.unit)

        # result = self.value * other.value
        result = super(Value, self).__mul__(other)
        result *= self.unit * other.unit
        result = Value(value=result.magnitude, unit=result.units)
        return result

    # function for adding
    def add(self, other):

        """
        Adds to values together

            :param self: Value instance
            :type self: physics.value.Value
            :param other: The object to be added
            :type other: Value, float, int, or np.ndarray:

            :returns Value: Returns a new Value object (or np.ndarray if other was np.ndarray)

            For Example::

            example = Value(value=1.0, unit=ureg.ohm)
            print(example.unit_str())
            'Ω'
        """
        return self.__add__(other)

    def __truediv__(self, other):
        if not isinstance(other, Value) and (isinstance(other, float) or isinstance(other, int)):
            return Value(value=super(Value, self).__truediv__(other), unit=self.unit)
        assert isinstance(other, Value), 'You can only multiple Values with other Values'
        # result = self.value * other.value
        result = super(Value, self).__truediv__(other)
        result *= (self.unit / other.unit)
        result = Value(value=result.magnitude, unit=result.units)
        return result

    def sqrt(self):
        a = self.unit**0.5
        return Value(value=self.value**0.5, unit=a)

    def __pow__(self, power, modulo=None):
        return Value(self.value**power, unit=self.unit**power)

    def unit_copy(self, other):
        assert isinstance(other, float) or isinstance(other, int), 'You can only create a value from a float or int'
        return Value(value=other, unit=self.unit)

    def __add__(self, other):
        if isinstance(other, np.ndarray):
            return other + np.array([self], dtype=object)

        if not isinstance(other, Value):
            return Value(value=other + self.value, unit=self.unit)

        assert other.unit.dimensionality == self.unit.dimensionality, 'You can only add values with the same dimensions'
        # result = super(Value, self).__add__(other)
        result = self.value*self.unit + other.value*other.unit
        # result *= self.unit * other.unit
        result = Value(value=result.magnitude, unit=result.units)
        return result

    def __sub__(self, other):
        if isinstance(other, np.ndarray):
            return other - np.array([self], dtype=object)
        if not isinstance(other, Value):
            return Value(value=other - self.value, unit=self.unit)
        # if isinstance(other, float) or isinstance(other, int):
        #     return Value(value=super(Value, self).__sub__(other), unit=self.unit)
        assert isinstance(other, Value), 'You can only multiple Values with other Values'
        assert other.unit.dimensionality == self.unit.dimensionality, 'You can only add values with the same dimensions'
        result = self.value*self.unit - other.value*other.unit
        result = Value(value=result.magnitude, unit=result.units)
        return result

# a = Value(8.0, ureg.ohm)
# d = 5.0
# c = a * d
# d = 5

