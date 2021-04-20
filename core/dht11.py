# dht11.py
# By: thekraftyman

import Adafruit_DHT as dht
from core.thermometer import Thermometer
from time import time, sleep
from core.util import load_config

class DHT11(Thermometer):

    def __init__(self, mode="F", time_delay=20):
        super().__init__(mode)
        self._time_delay = time_delay
        self._sensor_type = 'DHT11'
        config = load_config()
        self.therm_pin = int(config['DHT11_pin'])
        self.init_fail = False
        self._last_called = time()
        self._temp = self._get_temp()

    def temp(self):
        ''' returns the float val of the temp (calls self._get_temp()) '''
        if ((time() - self._last_called) < self._time_delay):
            return self._temp
        self._last_called = time()
        return self._get_temp()

    def _get_temp(self):
        ''' returns the float val of the temperature '''
        if self.init_fail:
            return -1
        temp_c, humidity = dht.read_retry(dht.DHT11,self.therm_pin)
        if self._mode.lower() == 'c':
            return float(temp_c)
        return float((temp_c * (9/5)) + 32)
