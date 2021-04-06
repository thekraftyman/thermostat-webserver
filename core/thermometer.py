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
        ''' returns the int val of the tempurature '''
        return int(self._temp())

    def temp(self):
        ''' returns the float val of the temperature '''
        pass
