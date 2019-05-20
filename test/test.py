from physics.value import Value, ureg
import numpy as np

def main():

    a = Value(value=3.0, unit=ureg.amp, name='input_voltage')
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
