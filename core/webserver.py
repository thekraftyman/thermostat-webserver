from flask import Flask, render_template
import datetime
import os
import platform
from json import dumps

# Check for a dev mode
if platform.system() in ['Darwin','Windows']:
    DEV_MODE = True

else:
    DEV_MODE = False

    from core.thermometer import Thermometer
    from core.hvac_controller import HVAC_Controller

class Webserver:

    def __init__(self,rx=0, tx=1, port=80, host='0.0.0.0', debug=False):
        self.template_path = os.path.abspath('templates')
        self.app = Flask(__name__, template_folder=self.template_path)
        self.port = port
        self.host = host
        self.debug = debug
        self.rx = rx
        self.tx = tx
        self.set_thermometer()
        self.set_hvac_controller()

    def set_thermometer(self, mode="F"):
        ''' sets up the thermometer '''
        if DEV_MODE:
            self.thermometer = 10
        else:
            self.thermometer = Thermometer(mode)

    def set_hvac_controller(self):
        ''' set up hvac controller '''
        if DEV_MODE:
            class fake_HVAC_Controller:
                def __init__(self):
                    self.mode = "OFF"
                    self.fan  = "OFF"
            self.hvac_controller = fake_HVAC_Controller()
        else:
            self.hvac_controller = HVAC_Controller(self.rx, self.tx)


    def run(self):
        self.add_routes()
        self.app.run(debug=self.debug, port=self.port, host=self.host)

    def add_routes(self):
        @self.app.route('/')
        def index():
            now = datetime.datetime.now()
            timeString = now.strftime("%Y-%m-%d %H:%M")
            templateData = {
                'title' : 'HELLO!',
                'time': timeString
            }
            return render_template('index.html', **templateData)

        @self.app.route('/stats')
        def stats():
            return dumps({'TEMP':str(self.thermometer), 'MODE':self.hvac_controller.mode, 'FAN':self.hvac_controller.fan})
