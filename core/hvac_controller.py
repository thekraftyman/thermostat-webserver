# hvac_controller.py
# By: Adam Kraft
from os import system
from time import sleep
from rgbled import RGBLED
from util import load_config

class HVAC_Controller:

    def __init__(self, temp_mode = "F"):
        self.temp_mode = temp_mode
        self.mode = None
        self.temp = None
        self.fan  = None
        self.is_on = None
        self._modes = ["off","cool","dry","heat","RESEND"]
        self._fan_speeds = ["auto","low","high"]
        self.load_from_config()
        self.indicator = RGBLED(self._red_pin, self._green_pin, self._blue_pin)

    def load_from_config(self):
        ''' loads the configuration for this unit '''
        json_dic = load_config()

        self.controller = json_dic['controller']
        self._red_pin = json_dic['red_pin']
        self._green_pin = json_dic['green_pin']
        self._blue_pin = json_dic['blue_pin']

    def send(self, mode, temp="18", fan='auto'):
        """ Send command to hvac """
        assert mode in self._modes
        assert fan in self._fan_speeds
        # Check for updated commands
        if temp != self.temp or mode != self.mode or fan != self.fan or mode == "RESEND":
            # Send the command
            if mode == "RESEND":
                self._send(self.mode, self.temp, self.fan)
            else:
                self._send(mode, temp, fan)

    def _send(self, mode, temp="18", fan='auto'):
        ''' more logic here '''
        command = f'irsend send_once {self.controller} '

        # put in the off button
        if mode == "off":
            system(command + 'turn-off')
            self.is_on = False
            return


        # make sure the mode will work
        if mode != self.mode and self.mode:
            system(command + f'turn-off')
            self.is_on = False
            sleep(4)

        # first, turn the device on
        if not self.is_on and mode != 'heat':
            system(command + f'{mode}-on')
            self.is_on = True
            sleep(4)

        # send the desired mode command
        command += f'{mode}-{fan}-{temp}{self.temp_mode}'

        # reassign the mode stuff
        self.temp = temp if (self.temp != temp) else self.temp
        self.mode = mode if (self.mode != mode) else self.mode
        self.fan  = fan if (self.fan != fan) else self.fan

        # send the command
        system(command)

    def __str__(self):
        ''' string of statuses '''
        toreturn  = "HVAC Controller with statuses:\n"
        toreturn += f"\tOn:   {self.is_on}\n"
        toreturn += f"\tMode: {self.mode}\n"
        toreturn += f"\tTemp: {self.temp}\n"
        toreturn += f"\tFan:  {self.fan}\n"
        return toreturn
