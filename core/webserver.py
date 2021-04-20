from flask import Flask, render_template, request
import datetime
import os
import platform
from json import dumps
from core.auth import Authenticator
from core.util import load_config
from core.thermometer import Thermometer
from core.dht11 import DHT11
from core.ds18b20 import DS18B20
from core.hvac_controller import HVAC_Controller

class Webserver:

    def __init__(self, port=80, host='0.0.0.0', debug=False):
        self.template_path = os.path.abspath('templates')
        self.static_path = os.path.abspath('src')
        self.app = Flask(__name__, static_folder=self.static_path, template_folder=self.template_path)
        self.port = port
        self.host = host
        self.debug = debug
        self.auth = Authenticator('hashed-api-key')
        self.set_thermometer()
        self.set_hvac_controller()
        self.add_routes()

    def set_thermometer(self, mode="F"):
        ''' sets up the thermometer '''
        config = load_config()
        sensor_type = config['temp_sensor_type'] if 'temp_sensor_type' in config else None

        # dht11 sensor
        if sensor_type.lower() == 'dht11' and bool(sensor_type):
            self.thermometer = DHT11(mode)

        # ds18b20
        elif sensor_type.lower() == 'ds18b20' and bool(sensor_type):
            self.thermometer = DS18B20(mode)

        # all others
        else:
            self.thermometer = Thermometer(mode)

    def set_hvac_controller(self):
        ''' set up hvac controller '''
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
            return render_template('index.html', **templateData)

        @self.app.route('/stats')
        def stats():
            return dumps({'TEMP':str(self.thermometer), 'MODE':self.hvac_controller.mode, 'FAN':self.hvac_controller.fan})

        @self.app.route('/set-api', methods=['GET','POST'])
        def set_api():
            # get any POST data (exit if none)
            if request.method != 'POST':
                return "POST Failure" if not self.debug else None

            try:
                request_data = request.get_json()
                if not bool(request_data):
                    raise Exception("Not json encoded")
            except:
                try:
                    request_data = request.form
                    if not bool(request_data):
                        raise Exception("Not form data")
                except:
                    return "Data Retrieval Failure"

            key  = request_data['key'] if 'key' in request_data else False
            temp = request_data['temp'] if 'temp' in request_data else False
            mode = request_data['mode'] if 'mode' in request_data else False
            fan  = request_data['fan'] if 'fan' in request_data else False

            # exit if no data there
            if True not in [bool(n) for n in [key,temp,mode,fan]]:
                return "No Data Failure" if not self.debug else None

            # exit if no key
            if not bool(key):
                return "No Key Failure" if not self.debug else None

            # compare api key
            if not self.auth.authenticate(key):
                return "Key Value Failure" if not self.debug else None

            # send data to the hvac controller
            self.hvac_controller.send(mode, temp, fan)

            # send success!
            return str(self.hvac_controller)

        @self.app.route('/set', methods=['GET','POST'])
        def set():
            # get GET data
            templateData = {
                'key'       : '',
                'key_type'  : '',
                'key_label' : 'Key:',
                'key_after' : '<br><br>'
            }

            if request.method == 'GET':
                request_data = request.args
                if 'key' in request_data:
                    templateData['key'] = request_data['key']
                    templateData['key_type'] = 'hidden'
                    templateData['key_label'] = ''
                    templateData['key_after'] = ''

            # Render template
            return render_template('set.html', **templateData)
