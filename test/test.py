from physics.value import Value, ureg


def main():

    a = Value(value=2.0, unit=ureg.volt, name='input_voltage')
    b = Value(value=2.0, unit=ureg.volt, name='input_current')
    d = a == b
    r = a.tensor
    d = 5


if __name__ == '__main__':
    main()
