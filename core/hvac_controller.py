# hvac_controller.py

__author__ = "thekraftyman"

from os import system
from time import sleep
from core.rgbled import RGBLED
import core.util as hvac_util

class HVAC_Controller:

    def __init__( self, temp_mode="F" ):
        # init some vars
        self.fan  = None
        self.mode = None
        self.temp = None
        self._allowed_modes = ["off","fan","cool","dry","heat","RESEND"]
        self._allowed_speeds = ["auto","low","high"]
        self._fan_temp = "64" if self.temp_mode == "F" else "30"
        self._is_on = None
        self._mode_indicators = {
            'cool': ( 0,  0, .5),
            'heat': (.8,  0,  0),
            'dry' : ( 0, .5,  0),
            'fan' : (.3, .3, .3)
        }
        self._temp_mode = temp_mode

        # run the stats
        self._init_stats()

        # set up the indicator and controller name
        json_dic = hvac_util.load_config()
        self.controller = json_dic['controller']
        if 'red_pin' in json_dic and 'green_pin' in json_dic and 'blue_pin' in json_dic:
            self.indicator = RGBLED( json_dic['red_pin'], json_dic['green_pin'], json_dic['blue_pin'] )
        else:
            self.indicator = None

    def _init_stats( self ):
        ''' reads the save-state.json file to populate the class variables '''
        state = hvac_util.load_state()
        self.mode = state['mode']
        self.temp = state['temp']
        self.fan  = state['fan']

        if self.mode == 'off' or not self.mode:
            self._is_on = False
        else:
            self._is_on = True

    def _save_state( self ):
        ''' saves the current params to the save-state.json file '''
        hvac_util.save_state({
            'mode': self.mode,
            'temp': self.temp,
            'fan' : self.fan
        })

    def _send_command( self, mode, temp="70", fan="auto" ):
        ''' send the command using irsend '''

        # turn on the unit if it is off
        if not self._is_on:
            self.turn_on( mode )

        # turn the unit off if required
        if mode == 'off':
            self.turn_off()
            return

        # restart the hvac with the new settings
        self.turn_off()
        command = f'irsend send_once {self.controller} '
        if mode == "fan":
            command += f'{mode}-{fan}-{self.fan_temp}{self._temp_mode}'
        else:
            command += f'{mode}-{fan}-{temp}{self._temp_mode}'
        system( command )

        # set the indicator
        if self.indicator:
            self.indicator.set( self._mode_indicators[mode] )

        # reassign the mode stuff
        self.temp = temp
        self.mode = mode
        self.fan = fan

        # save the save_state json file
        self._save_state()

    def turn_off( self ):
        ''' turn off the unit '''
        command = f'irsend send_once {self.controller} turn-off'
        self._is_on = False
        self.mode = 'off'
        if self.indicator:
            self.indicator.off()
        system( command )
        sleep(4)

    def turn_on( self, mode ):
        command = f'irsend send_once {self.controller} {mode}-on'
        self._is-on = True
        system( command )
        sleep(4)
