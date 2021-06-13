# hvac_controller.py
# By: thekraftyman
from os import system
from time import sleep
from core.rgbled import RGBLED
from core.util import load_config, load_state, save_state

class HVAC_Controller:

    def __init__(self, temp_mode = "F"):
        self.temp_mode = temp_mode
        self.fan_temp = "64" if self.temp_mode == "F" else "30"
        self.mode = None
        self.temp = None
        self.fan  = None
        self.is_on = None
        self._init_stats()
        self._modes = ["off","fan","cool","dry","heat","RESEND"]
        self._fan_speeds = ["auto","low","high"]
        self._mode_indicators = {
            'cool': ( 0,  0, .5),
            'heat': (.8,  0,  0),
            'dry' : ( 0, .5,  0),
            'fan' : (.3, .3, .3)
        }
        self.load_from_config()
        self.init_indicator()

    def _init_stats(self):
        '''reads the save-state.json file to populate the class variables'''
        var_dic = load_state()
        self.mode = var_dic['mode']
        self.temp = var_dic['temp']
        self.fan  = var_dic['fan']

        if self.mode == "off" or not self.mode:
            self.is_on = False
        else:
            self.is_on = True

    def _save_state(self):
        ''' saves the hvac params to the save-state.json file '''

        save_state({
            'mode': self.mode,
            'temp': self.temp,
            'fan' : self.fan
        })


    def init_indicator(self):
        ''' initializes an indicator if rgb pins are specified in the config '''
        if self._red_pin and self._green_pin and self._blue_pin:
            # set up the led
            self.indicator = RGBLED(self._red_pin, self._green_pin, self._blue_pin)

        else:
            self.indicator = None

    def load_from_config(self):
        ''' loads the configuration for this unit '''
        json_dic = load_config()

        self.controller = json_dic['controller']
        self._red_pin = json_dic['red_pin'] if 'red_pin' in json_dic else None
        self._green_pin = json_dic['green_pin'] if 'green_pin' in json_dic else None
        self._blue_pin = json_dic['blue_pin'] if 'blue_pin' in json_dic else None

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
            self.mode = 'off'
            if self.indicator:
                self.indicator.off()

        else:
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
            if mode == 'fan':
                command += f'{mode}-{fan}-{self.fan_temp}{self.temp_mode}'
            else:
                command += f'{mode}-{fan}-{temp}{self.temp_mode}'

            # reassign the mode stuff
            self.temp = temp if (self.temp != temp) else self.temp
            self.mode = mode if (self.mode != mode) else self.mode
            self.fan  = fan if (self.fan != fan) else self.fan

            # set the indicator
            if self.indicator:
                self.indicator.set(self._mode_indicators[mode])

            # send the command
            system(command)

        # set the save_state.json file
        self._save_state()


    def __str__(self):
        ''' string of statuses '''
        toreturn  = "HVAC Controller with statuses:\n"
        toreturn += f"\tOn:   {self.is_on}\n"
        toreturn += f"\tMode: {self.mode}\n"
        toreturn += f"\tTemp: {self.temp}\n"
        toreturn += f"\tFan:  {self.fan}\n"
        return toreturn
