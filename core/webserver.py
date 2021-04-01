from flask import Flask, render_template
import datetime
import os

class Webserver:

    def __init__(self, port=80, host='0.0.0.0', debug=False):
        self.template_path = os.path.abspath('templates')
        print(self.template_path)
        self.app = Flask(__name__, template_folder=self.template_path)
        self.port = port
        self.host = host
        self.debug = debug

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
