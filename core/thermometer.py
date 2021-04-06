# thermometer.py
# By: Adam Kraft

class Thermometer:

    def __init__(self, pin, mode="F"):
        self._pin = pin
        self._mode = mode

    def __float__(self):
        ''' returns the float val of the temperature '''
        return float(self.temp())

    def __int__(self):
        return int(self.temp())

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

    def temp(self):
        ''' returns the float val of the temperature '''
        pass
