from physics.value import Value, ureg, MetaValue
from physics.fields import Field
import numpy as np
import unittest


class TestPhysicsPackage(unittest.TestCase):

    def test_value(self):

        # test the array_like function
        a = np.array([1, 2, 3, 4])
        b = Value.array_like(array=a, unit=ureg.amp)
        self.assertEquals(Value(1, ureg.amp), b[0], 'Error in Value.array_like()')

        a = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
        b = Value.array_like(array=a, unit=ureg.amp)
        self.assertEquals(Value(1, ureg.amp), b[0][0], 'Error in Value.array_like()')

        # test math operations
        a = Value(1, ureg.amp)
        a_n = 1
        b = Value(2, ureg.amp)
        c = Value(3, ureg.amp)
        d = Value(4, ureg.volt)
        e = Value(2, ureg.ohm)

        # test the add function
        self.assertEqual(c, a + b, 'Error in Value.__add__()')

        # test the subtract function
        self.assertEqual(c - b, a, 'Error in Value.__sub__()')

        # test the multiply function
        self.assertEqual(d, b * e, 'Error in Value.__mul__()')
        self.assertEqual(a, a * a_n, 'Error in Value.__mul__()')

        # test the divide function
        self.assertEqual(d / e, b, 'Error in Value.__truediv__()')
        self.assertEqual(a, a / a_n, 'Error in Value.__truediv__()')

        f = Field(field='voltage', name='nothing')
        print(f)
        a = Value(value=3.0, unit=ureg.amp, name='input_voltage', tf_shape=(None, 1))
        c = 1/a
        array = np.array([a, a, a], dtype=object)
        b = Value(value=2.0, unit=ureg.volt*ureg.volt, name='input_current')
        d = ureg.amp * array
        r = array * b
        f = b * array
        boo = r == f
        tmep = 1.0*ureg.volt
        f = 2.0*ureg.microvolt
        temp = tmep + f
        temp = tmep.to_reduced_units()
        d = a*2.0
        f = 2.0*a
        c = 1.0
        r = 1.0*ureg.volt
        t = ureg.volt * 1.0
        d = a == b
        r = a.tensor
        d = 5

    def test_metavalue(self):

        class MetaValueTest(MetaValue):

            def __init__(self, value):
                self.value = value

        # test math operations
        a = Value(1, ureg.amp)
        a_meta = MetaValueTest(Value(1, ureg.amp))
        a_n = 1
        b = Value(2, ureg.amp)
        b_meta = MetaValueTest(b)
        c = Value(3, ureg.amp)
        c_meta = MetaValueTest(c)
        d = Value(4, ureg.volt)
        d_meta = MetaValueTest(d)
        e = Value(2, ureg.ohm)
        e_meta = MetaValueTest(e)

        # test the add function
        self.assertEqual(c, b + a_meta, 'Error in MetaValue.__add__()')
        self.assertEqual(c, a_meta + b_meta, 'Error in MetaValue.__add__()')

        # test the subtract function
        self.assertEqual(c - b, a_meta, 'Error in MetaValue.__sub__()')
        self.assertEqual(c - b_meta, a_meta, 'Error in MetaValue.__sub__()')

        # test the multiply function
        self.assertEqual(d, b * e_meta, 'Error in MetaValue.__mul__()')
        self.assertEqual(a, a * a_n, 'Error in MetaValue.__mul__()')

        # test the divide function
        self.assertEqual(d / e_meta, b, 'Error in MetaValue.__truediv__()')
        self.assertEqual(d_meta / e_meta, b, 'Error in MetaValue.__truediv__()')
        self.assertEqual(a, a / a_n, 'Error in MetaValue.__truediv__()')