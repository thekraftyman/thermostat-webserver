from flask import Flask, render_template
import datetime
import os
import platform

# Check for a dev mode
if platform.system() in ['Darwin','Windows']:
    DEV_MODE = True

else:
    DEV_MODE = False

    from core.thermometer import Thermometer
    from core.hvac_controller import HVAC_Controller

class Webserver:

    def __init__(self, port=80, host='0.0.0.0', debug=False):
        self.template_path = os.path.abspath('templates')
        self.app = Flask(__name__, template_folder=self.template_path)
        self.port = port
        self.host = host
        self.debug = debug

    def set_thermometer(self, pin, mode="F"):
        ''' sets up the thermometer with given pin '''
        self._thermo_pin = pin
        if DEV_MODE:
            self.thermometer = 10
        else:
            self.thermometer = Thermometer(pin, mode)

    def set_hvac_controller(self, rx, tx):
        pass


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
