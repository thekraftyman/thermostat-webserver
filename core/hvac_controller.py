self.temp# hvac_controller.py
# By: Adam Kraft
import json
from os import system

class HVAC_Controller:

    def __init__(self, rx, tx, temp_mode = "c"):
        self._rx = rx
        self._tx = tx
        self.temp_mode = temp_mode
        self.mode = None
        self.temp = None
        self.fan  = None
        self._modes = {
            "OFF"    :  0,
            "COOL"   :  1,
            "DRY"    :  2,
            "HEAT"   :  3,
            "RESEND" : -1
        }
        self._fan_speeds = {
            "AUTO" : 0,
            "LOW"  : 1,
            "HIGH" : 2
        }
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
        system(build_command(temp, mode, fan))

    def build_command(self, temp, mode, fan):
        ''' builds the command that will be sent to the hvac unit '''
        return f'irsend send_once {self.controller} {mode}-{fan}-{temp}{self.temp_mode}'
