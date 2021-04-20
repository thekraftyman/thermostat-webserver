# ds18b20.py
# By: thekraftyman

from os import system
from glob import glob
import time

class DS18B20(Thermometer):

    def __init__(self, mode="F"):
        super().__init__(mode)
        self._sensor_type = 'ds18b20'
        try:
            system('modprobe w1-gpio')
            system('modprobe w1-therm')
            self.base_dir = '/sys/bus/w1/devices/'
            self.device_folder = glob(self.base_dir + '28*')[0]
            self.device_file = self.device_folder + '/w1_slave'
            with open(self.device_file,'r') as infile:
                pass
            self.init_fail = False
        except:
            self.init_fail = True

    def temp(self):
        ''' returns the float val of the temperature '''
        if self.init_fail:
            return -1
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
