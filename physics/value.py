# H1 -- For the Value class
# *************************
from physics.units import complete_units, ureg, pint_to_str, str_to_pint
import pint
import numpy as np
import physics.conf as conf

if conf.tf_flag:
    import tensorflow as tf

# H3 -- Value Class
# -----------------


class Value(float):

    """Value object built on the float object and using `Pint Units <https://pint.readthedocs.io/en/0.9/>`_.

        Args:
            value (float): The float value
            unit (pint.unit._Unit, optional): The unit for this value.  Default is dimensionless ('')
            name (str, optional): The name of the value.  Default is None but needed to create a tensor for the Value instance
            tf_shape (tuple, optional): The shape of the tensor

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

    def __new__(cls, value, unit=ureg.dimensionless, tf_shape=None, name=None):
        # assert unit in complete_units, 'Your unit {0} is not in the list of available units'.format(unit)
        # value, unit = cls.SI_unit(value, unit)
        return float.__new__(cls, value)

    # return an np.ndarray of values given a unit and ndarray
    @classmethod
    def array_like(cls, array, unit):
        """
        Converts all the floats in array to Values
        Args:
            array (np.ndarray): The array to be converted. Should be either 1D or 2D
            unit (urge.unit): The desired unit for all the values

        Returns:
            np.ndarray with the new units
        """
        if len(array.shape) == 1:
            result = np.array([Value(value=x, unit=unit) for x in array], dtype=object)
        elif len(array.shape) == 2:
            result = np.array([[Value(value=x, unit=unit) for x in sub] for sub in array], dtype=object)
        else:
            raise ValueError('You are trying to convert an array with rank {0}, but only arrays with 1 or 2 dims'
                             ' can be converted right now.'.format(len(array.shape)))
        return result

    def unit_str(self):

        """Gives the str of the unit.

            :returns str: A string of the unit

            For Example::

            example = Value(value=1.0, unit=ureg.ohm)
            print(example.unit_str())
            Ohm
            """
        a = pint_to_str(self.unit)
        return a

    def __str__(self):
        return '{0} '.format(self.value) + self.unit_str()

    def __init__(self, value, unit=ureg.dimensionless, name=None, tf_shape=None):
        if unit is None:
            unit = ureg.dimensionless
        assert isinstance(unit, pint.unit._Unit), 'You must create a value with a unit form physics.value.ureg. See Docs for details.'
        float.__init__(value)
        # make sure this is the simplest form
        # test = value * unit
        # test.to_reduced_units()
        self.unit = unit
        self.value = value
        self.name = name
        # if the tf flag is raised and a name is give, then create a placeholder
        if conf.tf_flag:
            if name is None:
                self.placeholder = None
            else:
                if tf_shape is None:
                    tf_shape = (None, 1)
                self.tf_shape = tf_shape
                self.placeholder = tf.placeholder(name=name, shape=self.tf_shape, dtype=conf.tf_dtype)

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

    def base_units(self):
        tmp = self.value * self.unit
        tmp = tmp.to_base_units()
        return Value(tmp.magnitude, tmp.units)

    def __round__(self, n=None):
        return Value(value=float.__round__(self, n), unit=self.unit)

    def __neg__(self):
        return Value(value=self.value*-1, unit=self.unit)

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

    # multiply is commutative
    __rmul__ = __mul__

    def __abs__(self):
        return Value(value=abs(self.value), unit=self.unit)

    def __truediv__(self, other):
        if isinstance(other, np.ndarray):
            return np.array([self], dtype=object) / other
        if not isinstance(other, Value) and (isinstance(other, float) or isinstance(other, int)):
            return Value(value=super(Value, self).__truediv__(other), unit=self.unit)
        assert isinstance(other, Value), 'You can only multiple Values with other Values'
        # result = self.value * other.value
        try:
            result = super(Value, self).__truediv__(other)
        except ZeroDivisionError:
            return np.inf
        result *= (self.unit / other.unit)
        result = Value(value=result.magnitude, unit=result.units)
        return result

    def __rtruediv__(self, other):
        if isinstance(other, np.ndarray):
            return other / np.array([self], dtype=object)
        if not isinstance(other, Value) and (isinstance(other, float) or isinstance(other, int)):
            return Value(value=super(Value, self).__rtruediv__(other), unit=(1/self.unit).units)
        assert isinstance(other, Value), 'You can only multiple Values with other Values'
        # result = self.value * other.value
        result = super(Value, self).__rtruediv__(other)
        result *= (other.unit / self.unit)
        result = Value(value=result.magnitude, unit=result.units)
        return result

    # this will force numpy to use my operators. May depreciate in the future
    __array_priority__ = 17

    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    def sqrt(self):
        a = self.unit**0.5
        return Value(value=self.value**0.5, unit=a)

    def __pow__(self, power, modulo=None):
        return Value(self.value**power, unit=self.unit**power)

    def unit_copy(self, other):
        assert not isinstance(other, Value), "You cannot create a value from another value"
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

    # reverse add is the same as forward add
    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, np.ndarray):
            return np.array([self], dtype=object) - other
        if not isinstance(other, Value):
            return Value(value=self.value - other, unit=self.unit)
        # if isinstance(other, float) or isinstance(other, int):
        #     return Value(value=super(Value, self).__sub__(other), unit=self.unit)
        assert isinstance(other, Value), 'You can only multiple Values with other Values'
        assert other.unit   .dimensionality == self.unit.dimensionality, 'You can only add values with the same dimensions'
        result = self.value*self.unit - other.value*other.unit
        result = Value(value=result.magnitude, unit=result.units)
        return result

    def __rsub__(self, other):
        result = self.__sub__(other)
        return result*-1

    def __eq__(self, other):
        # Check they are both values
        if isinstance(other, Value):
            # check they are the same
            return self.value*self.unit == other.value*other.unit
        # if other is not unit, then they are not the same
        else:
            return False

    def __gt__(self, other):
        # Check they are both values
        if isinstance(other, Value):
            # check they are the same
            return self.value * self.unit > other.value * other.unit
        # if other is not unit, then they are not the same
        else:
            return False

    def __lt__(self, other):
        # Check they are both values
        if isinstance(other, Value):
            # check they are the same
            return self.value * self.unit < other.value * other.unit
        # if other is not unit, then they are not the same
        else:
            return False

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    # the copy value function. Used for taking an __input Value but keeping the tensor
    def copy_value(self, __input):
        assert isinstance(__input, Value), 'You can only copy_value from a Value instance'
        self.value = __input.value
        self.unit = __input.unit

    # np functions
    def log10(self):
        return Value(value=np.log10(self.value), unit=self.unit)

    # define some properties
    @property
    def __tensor(self):
        assert self.placeholder is not None, 'This value does not have a tensor. Be sure the conf.tf_flag is True and a name was given ' \
                                             'for the Value instance.'
        return self.placeholder

    # get the value output
    @__tensor.getter
    def tensor(self):
        # if self.__value is None:
        #     raise ValueError('You have not set the value')
        return self.__tensor

    @property
    def tf_feed(self):
        newshape = np.ones_like(self.tf_shape)
        return np.reshape(np.array(self.value), newshape=newshape)

    def __setstate__(self, state):
        self.unit, self.value, self.name, self.placeholder = state
        # if the placeholder is not None, then import it from the default graph
        if self.placeholder is not None:
            graph = tf.get_default_graph()
            self.placeholder = graph.get_tensor_by_name(self.placeholder)

    def __getstate__(self):
        if self.placeholder is not None:
            return self.unit, self.value, self.name, self.placeholder.name
        else:
            return self.unit, self.value, self.name, None

    def __hash__(self):
        # hash for Value is the just the float value
        return str(self.value)
    # # create a copy property used for copying a value over
    # @property
    # def copy(self):
    #     return None
    #
    # @copy.setter
    # def copy(self, _input):
    #
    #     assert isinstance(_input, Value), 'The given copy object should be of type Value.'
    #
    #     if _input.placeholder is None:
    #         tmp = self.placeholder
    #
    #     self = _input
    #
    #



        # if self.__value is None:
        #     raise ValueError('You have not set the value')
