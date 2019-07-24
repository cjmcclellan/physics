

class Material(object):

    def __init__(self, name, thermal_conductivity):
        # save the name
        self.name = name
        self.thermal_conductivity = thermal_conductivity


class Metal(Material):

    def __init__(self, *args, **kwargs):
        super(Metal, self).__init__(*args, **kwargs)


class Semiconductor(Material):

    def __init__(self, bandgap, dielectric, *args, **kwargs):
        super(Semiconductor, self).__init__(*args, **kwargs)
        # save the bandgap
        self.bandgap = bandgap
        self.dielectric = dielectric


class Insulator(Semiconductor):

    def __init__(self, *args, **kwargs):
        super(Semiconductor, self).__init__(*args, **kwargs)

