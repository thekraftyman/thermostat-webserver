# dht11.py
# By: thekraftyman

from pigpio-dht import DHT11 as pigpio_DHT11
from core.thermometer import Thermometer
from time import time, sleep
from core.util import load_config

class DHT11(Thermometer):

    def __init__(self, mode="F", time_delay=10):
        super().__init__(mode)
        self._time_delay = time_delay
        self._sensor_type = 'DHT11'
        config = load_config()
        self.therm_pin = int(config['DHT11_pin'])
        self.init_fail = False
        self._dht11 = pigpio_DHT11(self.therm_pin)
        self._last_called = time()
        self._temp = self._get_temp()

    def temp(self):
        ''' returns the float val of the temp (calls self._get_temp()) '''
        if ((time() - self._last_called) < self._time_delay):
            return self._temp
        self._last_called = time()
        self._temp = self._get_temp()
        return self._temp

    def _get_temp(self):
        ''' returns the float val of the temperature '''
        if self.init_fail:
            return -1
        try:
            sense_out = self._dht11.read()
        except RuntimeError:
            sense_out = {'temp_c': -1.0, 'temp_f': -1.0, 'humidity': -1, 'valid': False}
        if self._mode.lower() == 'c':
            return float(sense_out['temp_c'])
        return sense_out['temp_f']
