# thermometer.py
# By: Adam Kraft
from os import system
from glob import glob
from time import sleep

class Thermometer:

    def __init__(self, mode="F"):
        self._mode = mode

        # set up one-wire
        system('modprobe w1-gpio')
        system('modprobe w1-therm')
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

    def temp(self):
        ''' returns the float val of the temperature '''
        lines = self._temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            if self._mode == "C":
                return temp_c
            return temp_c * 9.0 / 5.0 + 32.0
        else:
            return 0.0

    def _temp_raw(self):
        ''' returns the lines of the tempurature file '''
        f = open(self.device_file, 'r')
        with open(self.device_file, 'r') as infile:
            lines = infile.readlines()
        return lines

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
