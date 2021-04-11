from flask import Flask, render_template, request
import datetime
import os
import platform
from json import dumps
from hashlib import sha256

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
        self.static_path = os.path.abspath('src')
        self.app = Flask(__name__, static_folder=self.static_path, template_folder=self.template_path)
        self.port = port
        self.host = host
        self.debug = debug
        self.set_thermometer()
        self.set_hvac_controller()
        self.add_routes()

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

                def send(self,*args, **kwargs):
                    pass

            self.hvac_controller = fake_HVAC_Controller()
        else:
            self.hvac_controller = HVAC_Controller()

    def run(self):
        self.app.run(debug=self.debug, port=self.port, host=self.host)

    def add_routes(self):
        @self.app.route('/', methods=['GET','POST'])
        def index():
            # GET any vars passed in the url
            title = request.args.get('title') if request.args.get('title') else "Hello!"

            # Get current time
            now = datetime.datetime.now()
            timeString = now.strftime("%Y-%m-%d %H:%M")
            templateData = {
                'title' : title,
                'time': timeString
            }
            return render_template('index.html', **templateData) + os.getcwd()

        @self.app.route('/stats')
        def stats():
            return dumps({'TEMP':str(self.thermometer), 'MODE':self.hvac_controller.mode, 'FAN':self.hvac_controller.fan})

        @self.app.route('/set', methods=['GET','POST'])
        def set():
            # get any POST data (exit if none)
            if request.method != 'POST':
                return "Failure"

            request_data = request.get_json()
            key  = request_data['key'] if 'key' in request_data else False
            temp = request_data['temp'] if 'temp' in request_data else False
            mode = request_data['mode'] if 'mode' in request_data else False
            fan  = request_data['fan'] if 'fan' in request_data else False

            # exit if no data there
            if True not in [bool(n) for n in [key,temp,mode,fan]]:
                return "Failure"

            # exit if no key
            if not bool(key):
                return "Failure"

            # compare api key
            with open('hashed-api-key','r') as infile:
                pre_hashed_key = infile.readline().strip()

            hashed_key = sha256(key.encode('ascii')).hexdigest()

            if hashed_key != pre_hashed_key:
                return "Failure"

            # send data to the hvac controller
            self.hvac_controller.send(mode, temp, fan)

            # send success!
            return "Success!"
