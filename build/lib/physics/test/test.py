from physics.value import Value, ureg
from physics.fields import Field
import numpy as np

def main():

    a = np.array([1, 2, 3, 4])
    b = Value.array_like(array=a, unit=ureg.amp)
    print(b[0])
    a = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
    b = Value.array_like(array=a, unit=ureg.amp)
    print(b[0][0])
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


if __name__ == '__main__':
    main()
