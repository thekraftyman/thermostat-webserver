# thermometer.py
# By: thekraftyman
from core.util import load_config

class Thermometer:

    def __init__(self, mode="F"):
        self._mode = mode

        config = load_config()
        self._sensor_type = config['temp_sensor_type'] if 'temp_sensor_type' in config else None
        self.init_fail = True

    def temp(self):
        ''' returns the float val of the temperature '''
        if self.init_fail:
            return -1

    def __float__(self):
        ''' returns the float val of the temperature '''
        return float(self.temp())

    def __int__(self):
        return int(self.temp())

    def __str__(self):
        return str(float(self))

    def __neg__(self):
        return - float(self)

    def __add__(self, other):
        return float(self) + other

    def __radd__(self, other):
        return other + float(self)

    def __sub__(self, other):
        return float(self) - other

    def __rsub__(self, other):
        return other - float(self)

    def __mul__(self, other):
        return float(self) * other

    def __rmul__(self, other):
        return other * float(self)

    def __div__(self, other):
        return float(self) / other

    def __rdiv__(self, other):
        return other / float(self)
