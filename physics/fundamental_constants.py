# just give fundamental constants
from physics.value import ureg, Value

free_space_permittivity_F_div_m = Value(value=8.85e-12, unit=ureg.farad/ureg.meter)
free_space_permittivity_F_div_cm = Value(value=8.85e-14, unit=ureg.farad/ureg.centimeter)

electron_charge_C = Value(value=1.602176634e-19, unit=ureg.coulomb)

