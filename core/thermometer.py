# thermometer.py
# By: Adam Kraft
from os import system
from glob import glob
from time import sleep
from core.util import load_config
from adafruit_dht import DHT11
import board

class Thermometer:

    def __init__(self, mode="F"):
        self._mode = mode

        config = load_config()
        self._sensor_type = config['temp_sensor_type'] if 'temp_sensor_type' in config else None
        self.init_fail = False

        # init DHT11
        if 'dht11' in self._sensor_type.lower():
            self._sensor_type = 'DHT11'
            self.therm_pin = config['DHT11_pin']
            dhtpins = {
                '1' : board.D1,
                '2' : board.D2,
                '3' : board.D3,
                '4' : board.D4,
                '5' : board.D5,
                '6' : board.D6,
                '7' : board.D7,
                '8' : board.D8,
                '9' : board.D9,
                '10': board.D10,
                '11': board.D11,
                '12': board.D12,
                '13': board.D13
            }
            self.dht_device = DHT11(dhtpins[self.therm_pin])

        # init ds18b20
        elif 'ds18b20' in self._sensor_type.lower():
            self._sensor_type = 'ds18b20'
            # set up one-wire
            try:
                system('modprobe w1-gpio')
                system('modprobe w1-therm')
                self.base_dir = '/sys/bus/w1/devices/'
                self.device_folder = glob(self.base_dir + '28*')[0]
                self.device_file = self.device_folder + '/w1_slave'
                with open(self.device_file,'r') as infile:
                    pass
            except:
                self.init_fail = True

        else:
            self.init_fail = True

    def temp(self):
        ''' returns the float val of the temperature '''
        if self.init_fail:
            return -1
        if self._sensor_type == 'DHT11':
            tries = 5
            for i in range(tries):
                try:
                    temp_c = self.dht_device.temperature
                    break
                except:
                    continue
            if not temp_c:
                raise Exception("Could not load data from DHT11 sensor")

            if self.mode.lower() == 'c':
                return float(temp_c)
            return float(temp_c * (9/5) + 32)

        elif self._sensor_type == 'ds18b20':
            lines = self.ds18b20_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = self.ds18b20_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                if self._mode == "C":
                    return temp_c
                return temp_c * 9.0 / 5.0 + 32.0
            else:
                return 0.0

    def ds18b20_temp_raw(self):
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
