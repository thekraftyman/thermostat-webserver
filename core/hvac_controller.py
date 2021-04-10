# hvac_controller.py
# By: Adam Kraft
import json
from os import system
from time import sleep

class HVAC_Controller:

    def __init__(self, rx, tx, temp_mode = "c"):
        self._rx = rx
        self._tx = tx
        self.temp_mode = temp_mode
        self.mode = None
        self.temp = None
        self.fan  = None
        self.is_on = None
        self._modes = ["OFF","COOL","DRY","HEAT","RESEND"]
        self._fan_speeds = ["AUTO","LOW","HIGH"]
        self.load_config()

    def load_config(self):
        ''' loads the configuration for this unit '''
        with open('config.json', 'r') as infile:
            json_dic = json.load(infile)

        self.controller = json_dic['controller']

    def send(self, temp, mode, fan):
        """ Send command to hvac """
        # Check for updated commands
        if temp != self.temp or mode != self.mode or fan != self.fan or mode == "RESEND":
            # Send the command
            if mode == "RESEND":
                self._send(self.temp, self.mode, self.fan)
            else:
                self._send(temp, mode, fan)

    def _send(self, temp, mode, fan):
        ''' more logic here '''
        command = f'irsend send_once {self.controller} '

        # make sure the mode will work
        if mode != self.mode and self.mode:
            system(command + f'turn-off')
            self.is_on = False
            sleep(2)

        # first, turn the device on
        if not self.is_on:
            sytem(command + f'{mode}-on')
            self.is_on = True
            sleep(2)

        # send the desired mode command
        command += f'{mode}-{fan}-{temp}{self.temp_mode}'

        # reassign the mode stuff
        self.temp = temp if (self.temp != temp) else self.temp
        self.mode = mode if (self.mode != mode) else self.mode
        self.fan  = fan if (self.fan != fan) else self.fan

        # send the command
        system(command)
